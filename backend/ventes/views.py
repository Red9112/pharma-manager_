import csv
from django.db.models import F
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import django_filters
from medicaments.models import Medicament

from .filters import VenteFilter
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
    filterset_class = VenteFilter

    def get_serializer_class(self):
        if self.action == "list":
            return VenteListSerializer
        return VenteSerializer

    def get_queryset(self):
        return super().get_queryset()

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

    @extend_schema(
        tags=["Ventes"],
        summary="Export CSV ventes",
        description="Exporte la liste des ventes (avec filtres date) en CSV.",
    )
    @action(detail=False, methods=["get"], url_path="export-csv")
    def export_csv(self, request):
        """Exporte les ventes en CSV."""
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="ventes.csv"'
        response.write("\ufeff")
        writer = csv.writer(response, delimiter=";")
        writer.writerow(["Référence", "Date", "Total TTC", "Statut", "Notes"])
        for v in self.filter_queryset(self.get_queryset()):
            writer.writerow([
                v.reference,
                v.date_vente.strftime("%Y-%m-%d %H:%M") if v.date_vente else "",
                v.total_ttc,
                v.get_statut_display() if hasattr(v, "get_statut_display") else v.statut,
                (v.notes or "")[:200],
            ])
        return response
