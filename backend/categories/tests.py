"""
Tests unitaires pour l'app categories.
"""
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Categorie


class CategorieModelTests(TestCase):
    """Tests du modèle Categorie."""

    def test_str_returns_nom(self):
        c = Categorie.objects.create(nom="Antibiotiques", description="")
        self.assertEqual(str(c), "Antibiotiques")


class CategorieAPITests(TestCase):
    """Tests des endpoints catégories."""

    def setUp(self):
        self.client = APIClient()

    def test_list_categories_returns_200(self):
        response = self.client.get("/api/v1/categories/")
        self.assertEqual(response.status_code, 200)

    def test_create_categorie_returns_201(self):
        payload = {"nom": "Antalgiques", "description": "Contre la douleur"}
        response = self.client.post("/api/v1/categories/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["nom"], "Antalgiques")
