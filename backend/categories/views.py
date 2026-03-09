from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from .models import Categorie
from .serializers import CategorieSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["Catégories"],
        summary="Liste des catégories",
        description="Liste de toutes les catégories de médicaments.",
    ),
    retrieve=extend_schema(tags=["Catégories"], summary="Détail d'une catégorie"),
    create=extend_schema(tags=["Catégories"], summary="Créer une catégorie"),
    update=extend_schema(tags=["Catégories"], summary="Modifier une catégorie"),
    partial_update=extend_schema(tags=["Catégories"], summary="Modification partielle"),
    destroy=extend_schema(tags=["Catégories"], summary="Supprimer une catégorie"),
)
class CategorieViewSet(viewsets.ModelViewSet):
    """
    ViewSet permettant de gérer les catégories de médicaments.

    Fournit un CRUD complet sur le modèle Categorie.
    """

    queryset = Categorie.objects.all().order_by("nom")
    serializer_class = CategorieSerializer

