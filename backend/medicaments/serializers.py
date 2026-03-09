from rest_framework import serializers

from .models import Medicament


class MedicamentSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Medicament.
    """

    class Meta:
        model = Medicament
        fields = [
            "id",
            "nom",
            "dci",
            "categorie",
            "forme",
            "dosage",
            "prix_achat",
            "prix_vente",
            "stock_actuel",
            "stock_minimum",
            "date_expiration",
            "ordonnance_requise",
            "est_actif",
            "date_creation",
            "est_en_alerte",
        ]
        read_only_fields = ["id", "date_creation", "est_en_alerte"]

    def validate_prix_achat(self, value):
        if value < 0:
            raise serializers.ValidationError("Le prix d'achat doit être positif.")
        return value

    def validate_prix_vente(self, value):
        if value < 0:
            raise serializers.ValidationError("Le prix de vente doit être positif.")
        return value

    def validate(self, attrs):
        stock_actuel = attrs.get("stock_actuel", 0)
        stock_minimum = attrs.get("stock_minimum", 0)
        if stock_actuel < 0 or stock_minimum < 0:
            raise serializers.ValidationError(
                "Les valeurs de stock doivent être supérieures ou égales à zéro."
            )
        return attrs

