from django.contrib import admin
from .models import Car, CarPrice

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("marque", "modele", "annee", "transmission", "ip", "categorie", "rarete", "prix_initial")
    list_filter = ("marque", "transmission", "categorie", "rarete")
    search_fields = ("marque", "modele")

@admin.register(CarPrice)
class CarPriceAdmin(admin.ModelAdmin):
    list_display = ("car", "prix", "date")
    list_filter = ("car__marque",)
    search_fields = ("car__marque", "car__modele")
