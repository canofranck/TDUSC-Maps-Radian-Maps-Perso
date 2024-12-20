from django.contrib import admin
from .models import Car, CarPrice, Reglage, Like,  CustomUser, Favorite, Trajet
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy  as _


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        "marque",
        "modele",
        "annee",
        "transmission",
        "ip",
        "categorie",
        "rarete",
        "prix_initial",
    )
    list_filter = ("marque", "transmission", "categorie", "rarete")
    search_fields = ("marque", "modele")


@admin.register(CarPrice)
class CarPriceAdmin(admin.ModelAdmin):
    list_display = ("car", "prix", "date")
    list_filter = ("car__marque",)
    search_fields = ("car__marque", "car__modele")


class ReglageAdminForm(ModelForm):
    class Meta:
        model = Reglage
        fields = "__all__"
        labels = {
            "rapport_final": "Rapport final (3 , 5)",
            "premiere_vitesse": "1ère vitesse",
            "deuxieme_vitesse": "2ème vitesse",
            "appui_aerodynamique_avant": "Appui aérodynamique Avant( -1 , 1 )",
            "appui_aerodynamique_arriere": "Appuiaerodynamique Arriere ( -1 , 1 )",
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        # if instance.car:
        #     configuration, created = (
        #         ConfigurationReglage.objects.get_or_create(car=instance.car)
        #     )
        #     instance.configurationreglage = configuration
        # else:
        #     raise ValidationError("La voiture doit être sélectionnée.")

        if commit:
            instance.save()
        return instance


@admin.register(Reglage)
class ReglageAdmin(admin.ModelAdmin):
    form = ReglageAdminForm
    list_display = [field.name for field in Reglage._meta.fields]
    list_filter = ("car_id__marque",)
    search_fields = ("car_id__modele",)
    fieldsets = [
        (
            "Informations générales",
            {"fields": ("car_id", "user_id", "description")},
        ),
        (
            "Boîte de vitesse",
            {
                "fields": (
                    "rapport_final",
                    "premiere_vitesse",
                    "deuxieme_vitesse",
                    "troisieme_vitesse",
                    "quatrieme_vitesse",
                    "cinquieme_vitesse",
                    "sixieme_vitesse",
                    "septieme_vitesse",
                    "huitieme_vitesse",
                )
            },
        ),
        (
            "Aérodynamisme",
            {
                "fields": (
                    "appui_aerodynamique_avant",
                    "appui_aerodynamique_arriere",
                )
            },
        ),
        (
            "Suspension et ressorts",
            {
                "fields": (
                    "taille_suspension_arriere",
                    "taille_suspension_avant",
                    "durete_ressorts_arriere",
                    "durete_ressorts_avant",
                )
            },
        ),
        (
            "Amortisseurs",
            {
                "fields": (
                    "compression_amortisseurs_avant",
                    "compression_amortisseurs_arriere",
                    "decompression_amortisseurs_avant",
                    "decompression_amortisseurs_arriere",
                )
            },
        ),
        (
            "Conduite sportive",
            {
                "fields": (
                    "acceleration_avant",
                    "deceleration_avant",
                    "freinage_avant",
                    "distribution_puissance_avant_arriere",
                    "acceleration_centrale",
                    "deceleration_centrale",
                    "freinage_central",
                    "acceleration_arriere",
                    "deceleration_arriere",
                    "freinage_arriere",
                    "durete_barre_antiroulis_avant",
                    "durete_barre_antiroulis_arriere",
                    "angle_carrossage_arriere",
                    "angle_carrossage_avant",
                    "pression_pneus_arriere",
                    "pression_pneus_avant",
                )
            },
        ),
        (
            "Freinage",
            {"fields": ("repartiteur_freinage_avant", "pression_freinage")},
        ),
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("car")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("reglage", "user", "created_at")


# @admin.register(ConfigurationReglage)
# class ConfigurationReglageAdmin(admin.ModelAdmin):
#     list_display = (
#         "car",
#         "rapport_final_min",
#         "rapport_final_max",
#         "background",
#     )  # Champs à afficher dans la liste
#     search_fields = ["car"]  # Champs pour la recherche


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "last_login",
        "is_superuser",
        "is_staff",
        "is_active",
        "reglage_is_active"
            )


admin.site.register(CustomUser, UserAdmin)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["user", "lat", "lng", "description"]

class TrajetAdmin(admin.ModelAdmin):
    list_display = ["user", "nom", "depart_lat", "depart_lng", "arrivee_lat", "arrivee_lng"]
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Trajet, TrajetAdmin)
