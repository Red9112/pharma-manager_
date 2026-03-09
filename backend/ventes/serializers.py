from django.db.models import F
from rest_framework import serializers
from medicaments.models import Medicament

from .models import LigneVente, Vente


class LigneVenteSerializer(serializers.ModelSerializer):
    """Serializer pour une ligne de vente (lecture ou écriture)."""

    medicament_nom = serializers.CharField(source="medicament.nom", read_only=True)

    class Meta:
        model = LigneVente
        fields = [
            "id",
            "medicament",
            "medicament_nom",
            "quantite",
            "prix_unitaire",
            "sous_total",
        ]
        read_only_fields = ["prix_unitaire", "sous_total", "medicament_nom"]

    def validate_quantite(self, value):
        if value <= 0:
            raise serializers.ValidationError("La quantité doit être strictement positive.")
        return value

    def validate_medicament(self, value):
        if not value.est_actif:
            raise serializers.ValidationError("Ce médicament n'est plus actif.")
        return value


class VenteSerializer(serializers.ModelSerializer):
    """Serializer pour une vente avec ses lignes."""

    lignes = LigneVenteSerializer(many=True)

    class Meta:
        model = Vente
        fields = [
            "id",
            "reference",
            "date_vente",
            "total_ttc",
            "statut",
            "notes",
            "lignes",
        ]
        read_only_fields = ["reference", "date_vente", "total_ttc"]

    def validate_lignes(self, value):
        if not value:
            raise serializers.ValidationError("Une vente doit contenir au moins une ligne.")
        for item in value:
            medicament = item.get("medicament")
            if medicament is None:
                raise serializers.ValidationError("Chaque ligne doit avoir un médicament.")
            if isinstance(medicament, int):
                medicament = Medicament.objects.filter(pk=medicament, est_actif=True).first()
                if not medicament:
                    raise serializers.ValidationError("Médicament invalide ou inactif.")
            qte = item.get("quantite", 0)
            if medicament.stock_actuel < qte:
                raise serializers.ValidationError(
                    f"Stock insuffisant pour {medicament.nom}: disponible {medicament.stock_actuel}, demandé {qte}."
                )
        return value

    def create(self, validated_data):
        lignes_data = validated_data.pop("lignes")
        vente = Vente.objects.create(**validated_data)
        for line in lignes_data:
            medicament = line["medicament"]
            quantite = line["quantite"]
            prix_unitaire = medicament.prix_vente
            LigneVente.objects.create(
                vente=vente,
                medicament=medicament,
                quantite=quantite,
                prix_unitaire=prix_unitaire,
            )
            Medicament.objects.filter(pk=medicament.pk).update(
                stock_actuel=F("stock_actuel") - quantite
            )
        vente.recalculer_total()
        return vente


class VenteListSerializer(serializers.ModelSerializer):
    """Serializer léger pour la liste des ventes."""

    class Meta:
        model = Vente
        fields = ["id", "reference", "date_vente", "total_ttc", "statut", "notes"]
