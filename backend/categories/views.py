from rest_framework import viewsets

from .models import Categorie
from .serializers import CategorieSerializer


class CategorieViewSet(viewsets.ModelViewSet):
    """
    ViewSet permettant de gérer les catégories de médicaments.

    Fournit un CRUD complet sur le modèle Categorie.
    """

    queryset = Categorie.objects.all().order_by("nom")
    serializer_class = CategorieSerializer

