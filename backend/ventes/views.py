from django.db.models import F
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from medicaments.models import Medicament

from .models import LigneVente, Vente
from .serializers import VenteListSerializer, VenteSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["Ventes"],
        summary="Historique des ventes",
        description="Liste paginée des ventes. Filtres : date_from, date_to (format AAAA-MM-JJ).",
    ),
    retrieve=extend_schema(tags=["Ventes"], summary="Détail d'une vente"),
    create=extend_schema(
        tags=["Ventes"],
        summary="Enregistrer une vente",
        description="Crée une vente avec ses lignes. Déduit automatiquement les quantités du stock. "
        "Chaque ligne doit contenir medicament (id) et quantite.",
    ),
    update=extend_schema(tags=["Ventes"], summary="Modifier une vente"),
    partial_update=extend_schema(tags=["Ventes"], summary="Modification partielle"),
    destroy=extend_schema(tags=["Ventes"], summary="Supprimer une vente"),
)
class VenteViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les ventes.
    - Liste et détail des ventes, filtrage par date.
    - Création avec déduction automatique du stock.
    - Action annuler : réintégration du stock et passage au statut Annulée.
    """

    queryset = Vente.objects.all().prefetch_related("lignes", "lignes__medicament")

    def get_serializer_class(self):
        if self.action == "list":
            return VenteListSerializer
        return VenteSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")
        if date_from:
            qs = qs.filter(date_vente__date__gte=date_from)
        if date_to:
            qs = qs.filter(date_vente__date__lte=date_to)
        return qs

    @extend_schema(
        tags=["Ventes"],
        summary="Annuler une vente",
        description="Réintègre les quantités dans le stock et passe le statut à Annulée. "
        "Retourne 400 si la vente est déjà annulée.",
        responses={
            200: VenteSerializer,
            400: {"description": "Vente déjà annulée"},
        },
    )
    @action(detail=True, methods=["post"], url_path="annuler")
    def annuler(self, request, pk=None):
        """
        Annule la vente : réintègre le stock des lignes et passe le statut à Annulée.
        Retourne 400 si la vente est déjà annulée.
        """
        vente = self.get_object()
        if vente.statut == Vente.Statut.ANNULEE:
            return Response(
                {"detail": "Cette vente est déjà annulée."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        for ligne in vente.lignes.select_related("medicament").all():
            Medicament.objects.filter(pk=ligne.medicament_id).update(
                stock_actuel=F("stock_actuel") + ligne.quantite
            )
        vente.statut = Vente.Statut.ANNULEE
        vente.save(update_fields=["statut"])
        serializer = self.get_serializer(vente)
        return Response(serializer.data)
