"""
Tests unitaires pour l'app medicaments.
"""
from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient

from categories.models import Categorie
from .models import Medicament


class MedicamentModelTests(TestCase):
    """Tests du modèle Medicament."""

    def setUp(self):
        self.cat = Categorie.objects.create(nom="TestCat", description="")

    def test_est_en_alerte_true_quand_stock_inferieur_ou_egal_minimum(self):
        m = Medicament.objects.create(
            nom="M1",
            dci="",
            categorie=self.cat,
            forme="Comprimé",
            dosage="500mg",
            prix_achat=Decimal("10"),
            prix_vente=Decimal("15"),
            stock_actuel=5,
            stock_minimum=10,
            date_expiration="2026-12-31",
        )
        self.assertTrue(m.est_en_alerte)

    def test_est_en_alerte_false_quand_stock_superieur_minimum(self):
        m = Medicament.objects.create(
            nom="M2",
            dci="",
            categorie=self.cat,
            forme="Comprimé",
            dosage="500mg",
            prix_achat=Decimal("10"),
            prix_vente=Decimal("15"),
            stock_actuel=20,
            stock_minimum=10,
            date_expiration="2026-12-31",
        )
        self.assertFalse(m.est_en_alerte)


class MedicamentAPITests(TestCase):
    """Tests des endpoints médicaments."""

    def setUp(self):
        self.client = APIClient()
        self.cat = Categorie.objects.create(nom="API Cat", description="")

    def test_list_medicaments_returns_200(self):
        response = self.client.get("/api/v1/medicaments/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)

    def test_create_medicament_returns_201(self):
        payload = {
            "nom": "Paracétamol",
            "dci": "Paracétamol",
            "categorie": self.cat.id,
            "forme": "Comprimé",
            "dosage": "500mg",
            "prix_achat": "5.00",
            "prix_vente": "8.00",
            "stock_actuel": 100,
            "stock_minimum": 10,
            "date_expiration": "2026-12-31",
        }
        response = self.client.post("/api/v1/medicaments/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["nom"], "Paracétamol")

    def test_alertes_returns_only_low_stock(self):
        Medicament.objects.create(
            nom="Low",
            categorie=self.cat,
            forme="Tab",
            dosage="1",
            prix_achat=Decimal("1"),
            prix_vente=Decimal("2"),
            stock_actuel=1,
            stock_minimum=10,
            date_expiration="2026-12-31",
        )
        response = self.client.get("/api/v1/medicaments/alertes/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
