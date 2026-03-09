from django.contrib import admin

from .models import Medicament


@admin.register(Medicament)
class MedicamentAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "dci",
        "categorie",
        "stock_actuel",
        "stock_minimum",
        "est_en_alerte",
        "est_actif",
    )
    list_filter = ("categorie", "est_actif")
    search_fields = ("nom", "dci")
    ordering = ("nom",)

