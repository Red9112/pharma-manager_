from django.db import models


class Categorie(models.Model):
    """
    Représente une catégorie de médicaments.

    Attributs:
        nom (str): Nom de la catégorie (ex: antibiotique, antalgique).
        description (str): Description optionnelle de la catégorie.
        date_creation (datetime): Horodatage automatique de création.
    """

    nom = models.CharField(max_length=150, unique=True, verbose_name="Nom")
    description = models.TextField(
        blank=True,
        verbose_name="Description",
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["nom"]

    def __str__(self) -> str:
        return self.nom

