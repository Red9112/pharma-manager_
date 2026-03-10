"""
Tests unitaires pour l'app ventes.
"""
from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient

from categories.models import Categorie
from medicaments.models import Medicament
from .models import LigneVente, Vente


class VenteModelTests(TestCase):
    """Tests du modèle Vente."""

    def setUp(self):
        self.cat = Categorie.objects.create(nom="Cat", description="")
        self.med = Medicament.objects.create(
            nom="Med",
            categorie=self.cat,
            forme="Tab",
            dosage="1",
            prix_achat=Decimal("10"),
            prix_vente=Decimal("15"),
            stock_actuel=50,
            stock_minimum=5,
            date_expiration="2026-12-31",
        )

    def test_vente_reference_auto_generee(self):
        v = Vente.objects.create(statut=Vente.Statut.COMPLETEE)
        self.assertTrue(v.reference.startswith("VNT-"))
        self.assertIn(str(v.date_vente.year), v.reference)

    def test_recalculer_total(self):
        v = Vente.objects.create(statut=Vente.Statut.COMPLETEE)
        LigneVente.objects.create(
            vente=v,
            medicament=self.med,
            quantite=2,
            prix_unitaire=Decimal("15"),
        )
        v.recalculer_total()
        self.assertEqual(v.total_ttc, Decimal("30.00"))


class VenteAPITests(TestCase):
    """Tests des endpoints ventes."""

    def setUp(self):
        self.client = APIClient()
        self.cat = Categorie.objects.create(nom="Cat", description="")
        self.med = Medicament.objects.create(
            nom="Med",
            categorie=self.cat,
            forme="Tab",
            dosage="1",
            prix_achat=Decimal("10"),
            prix_vente=Decimal("15"),
            stock_actuel=50,
            stock_minimum=5,
            date_expiration="2026-12-31",
        )

    def test_list_ventes_returns_200(self):
        response = self.client.get("/api/v1/ventes/")
        self.assertEqual(response.status_code, 200)

    def test_create_vente_returns_201_and_deduits_stock(self):
        payload = {
            "notes": "",
            "lignes": [{"medicament": self.med.id, "quantite": 2}],
        }
        response = self.client.post("/api/v1/ventes/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("reference", response.data)
        self.med.refresh_from_db()
        self.assertEqual(self.med.stock_actuel, 48)
