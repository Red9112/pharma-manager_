"""
Filtres avancés pour les ventes.
"""
import django_filters
from .models import Vente


class VenteFilter(django_filters.FilterSet):
    """Filtres : statut, date."""

    statut = django_filters.ChoiceFilter(choices=Vente.Statut.choices)
    date_from = django_filters.DateFilter(field_name="date_vente__date", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="date_vente__date", lookup_expr="lte")

    class Meta:
        model = Vente
        fields = ["statut", "date_from", "date_to"]
