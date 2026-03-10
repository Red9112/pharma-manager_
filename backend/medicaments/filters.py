"""
Filtres avancés pour les médicaments.
"""
import django_filters
from .models import Medicament


class MedicamentFilter(django_filters.FilterSet):
    """Filtres avancés : catégorie."""

    categorie = django_filters.NumberFilter(field_name="categorie_id")

    class Meta:
        model = Medicament
        fields = ["categorie"]
