from decimal import Decimal
from django.db import models
from django.db.models import Max
from django.utils import timezone


def _generer_reference():
    """Génère une référence unique du type VNT-YYYY-NNNN."""
    annee = timezone.now().year
    dernier = (
        Vente.objects.filter(reference__startswith=f"VNT-{annee}-")
        .aggregate(m=Max("reference"))["m"]
    )
    if dernier:
        num = int(dernier.split("-")[-1]) + 1
    else:
        num = 1
    return f"VNT-{annee}-{num:04d}"


class Vente(models.Model):
    """
    Représente une transaction de vente.
    Le total_ttc est calculé automatiquement à partir des lignes de vente.
    """

    class Statut(models.TextChoices):
        EN_COURS = "en_cours", "En cours"
        COMPLETEE = "completee", "Complétée"
        ANNULEE = "annulee", "Annulée"

    reference = models.CharField(
        max_length=50, unique=True, blank=True, verbose_name="Référence"
    )
    date_vente = models.DateTimeField(verbose_name="Date de vente", auto_now_add=True)
    total_ttc = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="Total TTC",
    )
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.COMPLETEE,
        verbose_name="Statut",
    )
    notes = models.TextField(blank=True, verbose_name="Notes")

    class Meta:
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"
        ordering = ["-date_vente"]

    def __str__(self) -> str:
        return f"{self.reference} ({self.date_vente})"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = _generer_reference()
        super().save(*args, **kwargs)

    def recalculer_total(self) -> None:
        """Recalcule total_ttc à partir des lignes de vente."""
        from django.db.models import Sum
        self.total_ttc = self.lignes.aggregate(s=Sum("sous_total"))["s"] or Decimal("0")
        self.save(update_fields=["total_ttc"])


class LigneVente(models.Model):
    """
    Une ligne d'une vente : médicament, quantité, prix unitaire au moment de la vente (snapshot).
    sous_total = quantite * prix_unitaire.
    """

    vente = models.ForeignKey(
        Vente,
        on_delete=models.CASCADE,
        related_name="lignes",
        verbose_name="Vente",
    )
    medicament = models.ForeignKey(
        "medicaments.Medicament",
        on_delete=models.PROTECT,
        related_name="lignes_vente",
        verbose_name="Médicament",
    )
    quantite = models.PositiveIntegerField(verbose_name="Quantité")
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix unitaire au moment de la vente",
    )
    sous_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Sous-total",
    )

    class Meta:
        verbose_name = "Ligne de vente"
        verbose_name_plural = "Lignes de vente"

    def __str__(self) -> str:
        return f"{self.vente.reference} - {self.medicament.nom} x{self.quantite}"

    def save(self, *args, **kwargs):
        if self.prix_unitaire is not None and self.quantite is not None:
            self.sous_total = self.prix_unitaire * self.quantite
        super().save(*args, **kwargs)
