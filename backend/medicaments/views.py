from django.db import models
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Medicament
from .serializers import MedicamentSerializer


class MedicamentViewSet(viewsets.ModelViewSet):
    """
    ViewSet permettant de gérer les médicaments.

    La suppression est réalisée via un soft delete (est_actif=False).
    Un endpoint supplémentaire /alertes/ expose les médicaments dont le stock
    est inférieur ou égal au seuil minimum.
    """

    serializer_class = MedicamentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nom", "dci"]
    ordering_fields = ["nom", "stock_actuel", "date_creation"]
    ordering = ["nom"]

    def get_queryset(self):
        """
        Retourne uniquement les médicaments actifs par défaut.
        """

        queryset = Medicament.objects.filter(est_actif=True)
        categorie_id = self.request.query_params.get("categorie")
        if categorie_id:
            queryset = queryset.filter(categorie_id=categorie_id)
        return queryset

    def perform_destroy(self, instance):
        """
        Soft delete: on passe est_actif à False au lieu de supprimer la ligne.
        """

        instance.est_actif = False
        instance.save(update_fields=["est_actif"])

    @action(detail=False, methods=["get"], url_path="alertes")
    def alertes_stock(self, request):
        """
        Retourne les médicaments dont le stock est inférieur ou égal au stock minimum.
        """

        queryset = self.get_queryset().filter(stock_actuel__lte=models.F("stock_minimum"))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

