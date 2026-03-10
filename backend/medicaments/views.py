import csv
import django_filters
from django.db import models
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import MedicamentFilter
from .models import Medicament
from .serializers import MedicamentSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["Médicaments"],
        summary="Liste des médicaments",
        description="Liste paginée des médicaments actifs. Filtres : search (nom, dci), categorie (id).",
    ),
    retrieve=extend_schema(tags=["Médicaments"], summary="Détail d'un médicament"),
    create=extend_schema(tags=["Médicaments"], summary="Créer un médicament"),
    update=extend_schema(tags=["Médicaments"], summary="Modifier un médicament"),
    partial_update=extend_schema(tags=["Médicaments"], summary="Modification partielle"),
    destroy=extend_schema(
        tags=["Médicaments"],
        summary="Supprimer (soft delete)",
        description="Désactive le médicament (est_actif=False) sans le supprimer.",
    ),
)
class MedicamentViewSet(viewsets.ModelViewSet):
    """
    ViewSet permettant de gérer les médicaments.

    La suppression est réalisée via un soft delete (est_actif=False).
    Un endpoint supplémentaire /alertes/ expose les médicaments dont le stock
    est inférieur ou égal au seuil minimum.
    """

    serializer_class = MedicamentSerializer
    filterset_class = MedicamentFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ["nom", "dci"]
    ordering_fields = ["nom", "stock_actuel", "date_creation"]
    ordering = ["nom"]

    def get_queryset(self):
        """Retourne les médicaments actifs (filtre categorie via filterset_class)."""
        return Medicament.objects.filter(est_actif=True)

    def perform_destroy(self, instance):
        """
        Soft delete: on passe est_actif à False au lieu de supprimer la ligne.
        """

        instance.est_actif = False
        instance.save(update_fields=["est_actif"])

    @extend_schema(
        tags=["Médicaments"],
        summary="Médicaments en alerte de stock",
        description="Retourne les médicaments dont le stock actuel est inférieur ou égal au seuil minimum.",
    )
    @action(detail=False, methods=["get"], url_path="alertes")
    def alertes_stock(self, request):
        """
        Retourne les médicaments dont le stock est inférieur ou égal au stock minimum.
        """
        queryset = self.get_queryset().filter(stock_actuel__lte=models.F("stock_minimum"))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=["Médicaments"],
        summary="Export CSV inventaire",
        description="Exporte la liste des médicaments (actifs) en CSV.",
    )
    @action(detail=False, methods=["get"], url_path="export-csv")
    def export_csv(self, request):
        """Exporte l'inventaire des médicaments en CSV."""
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="inventaire_medicaments.csv"'
        response.write("\ufeff")  # BOM UTF-8 pour Excel
        writer = csv.writer(response, delimiter=";")
        writer.writerow(
            ["Nom", "DCI", "Catégorie", "Forme", "Dosage", "Prix achat", "Prix vente", "Stock", "Stock min", "Date expiration"]
        )
        for m in self.get_queryset().select_related("categorie"):
            writer.writerow([
                m.nom,
                m.dci or "",
                m.categorie.nom,
                m.forme,
                m.dosage,
                m.prix_achat,
                m.prix_vente,
                m.stock_actuel,
                m.stock_minimum,
                m.date_expiration,
            ])
        return response

