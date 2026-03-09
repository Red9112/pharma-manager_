from django.contrib import admin
from .models import LigneVente, Vente


class LigneVenteInline(admin.TabularInline):
    model = LigneVente
    extra = 0


@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display = ("reference", "date_vente", "total_ttc", "statut")
    list_filter = ("statut",)
    inlines = [LigneVenteInline]
    readonly_fields = ("reference", "date_vente", "total_ttc")
