from django.db import models
from django.utils import timezone
from authentication.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
import os
from tduscmap import settings

class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="favorites"
    )
    lat = models.FloatField()  # Latitude
    lng = models.FloatField()  # Longitude
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s favorite at ({self.lat}, {self.lng})"


class Car(models.Model):
    MARQUES = [
        ("Abarth", "Abarth"),
        ("AC", "AC"),
        ("Alfa Romeo", "Alfa Romeo"),
        ("Alpine", "Alpine"),
        ("Apollo Automobil", "Apollo Automobil"),
        ("Aston Martin", "Aston Martin"),
        ("Audi", "Audi"),
        ("Bentley", "Bentley"),
        ("BMW", "BMW"),
        ("Bugatti", "Bugatti"),
        ("Caterham", "Caterham"),
        ("Chevrolet", "Chevrolet"),
        ("Citroën", "Citroën"),
        ("Dodge", "Dodge"),
        ("Ferrari", "Ferrari"),
        ("Ford", "Ford"),
        ("Jaguar", "Jaguar"),
        ("Koenigsegg", "Koenigsegg"),
        ("Lamborghini", "Lamborghini"),
        ("Land Rover", "Land Rover"),
        ("Lancia", "Lancia"),
        ("Lotus", "Lotus"),
        ("Maserati", "Maserati"),
        ("McLaren", "McLaren"),
        ("MercedesAMG", "MercedesAMG"),
        ("MercedesBenz", "MercedesBenz"),
        ("Mini", "Mini"),
        ("Nissan", "Nissan"),
        ("Porsche", "Porsche"),
        ("Shelby", "Shelby"),
        ("Sientero", "Sientero"),
        ("WMotors", "WMotors"),
        ("Volkswagen", "Volkswagen"),
        ("W Motors", "W Motors"),
    ]
    TRANSMISSIONS = [
        ("RWD", "RWD"),
        ("FWD", "FWD"),
        ("4WD", "4WD"),
    ]

    CATEGORIES = [
        ("A", "Catégorie A"),
        ("B", "Catégorie B"),
        ("C", "Catégorie C"),
        ("D", "Catégorie D"),
        ("E", "Catégorie E"),
        ("F", "Catégorie F"),
        ("G", "Catégorie G"),
        ("H", "Catégorie H"),
    ]

    RARETES = [
        ("légendaire", "Légendaire"),
        ("épique", "Épique"),
        ("rare", "Rare"),
        ("commun", "Commun"),
        ("peu commun", "Peu commun"),
        (None, "Aucune"),
    ]

    marque = models.CharField(max_length=50, choices=MARQUES)
    modele = models.CharField(max_length=50)
    annee = models.PositiveIntegerField(null=True)
    transmission = models.CharField(
        max_length=3, choices=TRANSMISSIONS, null=True
    )
    ip = models.PositiveIntegerField(null=True)
    categorie = models.CharField(max_length=1, choices=CATEGORIES, null=True)
    rarete = models.CharField(
        max_length=10, choices=RARETES, blank=True, null=True
    )
    prix_initial = models.PositiveIntegerField(null=True)

    nb_vitesse = models.IntegerField(default=6, validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.annee})"


class CarPrice(models.Model):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="historique_prix"
    )
    prix = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return (
            f"{self.car.marque} {self.car.modele} - {self.date}: "
            f"{self.prix}€"
        )


# class ConfigurationReglage(models.Model):

#     car = models.ForeignKey(Car, on_delete=models.CASCADE)
#     # Champs spécifiques pour la configuration
#     rapport_final_min = models.DecimalField(
#         max_digits=5, decimal_places=2, null=True, blank=True
#     )
#     rapport_final_max = models.DecimalField(
#         max_digits=5, decimal_places=2, null=True, blank=True
#     )
#     premiere_vitesse_min = models.DecimalField(
#         max_digits=4, decimal_places=2, null=True, blank=True
#     )
#     premiere_vitesse_max = models.DecimalField(
#         max_digits=4, decimal_places=2, null=True, blank=True
#     )
#     deuxieme_vitesse_min = models.DecimalField(
#         max_digits=4, decimal_places=2, null=True, blank=True
#     )
#     deuxieme_vitesse_max = models.DecimalField(
#         max_digits=4, decimal_places=2, null=True, blank=True
#     )
#     troisieme_vitesse_min = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     troisieme_vitesse_max = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     quatrieme_vitesse_min = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     quatrieme_vitesse_max = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     cinquieme_vitesse_min = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     cinquieme_vitesse_max = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     sixieme_vitesse_min = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     sixieme_vitesse_max = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     septieme_vitesse_min = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     septieme_vitesse_max = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     huitieme_vitesse_min = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     huitieme_vitesse_max = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     taille_suspension_arriere_min = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     taille_suspension_arriere_max = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     taille_suspension_avant_min = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     taille_suspension_avant_max = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     acceleration_avant_min = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     acceleration_avant_max = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     deceleration_avant_min = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     deceleration_avant_max = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     freinage_avant_min = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     freinage_avant_max = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     distribution_puissance_avant_arriere_min = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     distribution_puissance_avant_arriere_max = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     acceleration_centrale_min = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     acceleration_centrale_max = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     deceleration_centrale_min = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     deceleration_centrale_max = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     freinage_centrale_min = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     freinage_centrale_max = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     pression_pneus_arriere_min = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     pression_pneus_arriere_max = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     pression_pneus_avant_min = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     pression_pneus_avant_max = models.DecimalField(
#         max_digits=6, decimal_places=2, null=True, blank=True
#     )
#     background = models.CharField(max_length=50, default='default_background')


class Reglage(models.Model):
    """Modèle pour stocker les réglages d'une voiture"""
    pieces = [
        ("Serie", "Serie"),
        ("Performance", "Perfomance"),
        ("Sport", "Sport"),
        ("Super Sport", "Super Sport"),
        ("Course", "Course"),
         ]
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    pieces = models.CharField(max_length=15, choices=pieces)
    # configurationreglage = models.ForeignKey(
    #     ConfigurationReglage, on_delete=models.CASCADE
    # )
    # vitesse
    # Boîte de vitesse
    rapport_final = models.DecimalField(max_digits=6, decimal_places=2)
    premiere_vitesse = models.DecimalField(max_digits=6, decimal_places=2)
    deuxieme_vitesse = models.DecimalField(max_digits=6, decimal_places=2)
    troisieme_vitesse = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    quatrieme_vitesse = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    cinquieme_vitesse = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    sixieme_vitesse = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    septieme_vitesse = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    huitieme_vitesse = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    neuvieme_vitesse = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    dixieme_vitesse = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )

    # Aérodynamisme
    appui_aerodynamique_avant = models.DecimalField(
        max_digits=3, decimal_places=2
    )
    appui_aerodynamique_arriere = models.DecimalField(
        max_digits=3, decimal_places=2
    )

    # Stabilité
    # hauteur de caisse
    taille_suspension_arriere = models.DecimalField(
        max_digits=6, decimal_places=2
    )
    taille_suspension_avant = models.DecimalField(
        max_digits=6, decimal_places=2
    )

    # Ressort
    durete_ressorts_arriere = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(80), MaxValueValidator(120)],
    )
    durete_ressorts_avant = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(80), MaxValueValidator(120)],
    )

    # Amortisseurs
    compression_amortisseurs_avant = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(80), MaxValueValidator(120)],
    )
    compression_amortisseurs_arriere = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(80), MaxValueValidator(120)],
    )
    decompression_amortisseurs_avant = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(80), MaxValueValidator(120)],
    )
    decompression_amortisseurs_arriere = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(80), MaxValueValidator(120)],
    )

    # tenue de route
    # differentiel_avant
    acceleration_avant = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    deceleration_avant = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    freinage_avant = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    # differentiel_central
    distribution_puissance_avant_arriere = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    acceleration_centrale = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    deceleration_centrale = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    freinage_central = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    # differentiel_arriere
    acceleration_arriere = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    deceleration_arriere = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    freinage_arriere = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    # barre anti roulis
    durete_barre_antiroulis_avant = models.DecimalField(
         max_digits=6, decimal_places=2, null=True, blank=True
    )
    durete_barre_antiroulis_arriere = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    # carrossge
    angle_carrossage_arriere = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(-6), MaxValueValidator(3)],
    )
    angle_carrossage_avant = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(-6), MaxValueValidator(3)],
    )
    # pression pneus
    pression_pneus_arriere = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    pression_pneus_avant = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )

    # Freinage
    repartiteur_freinage_avant = models.DecimalField(
         max_digits=6, decimal_places=2, null=True, blank=True
    )
    pression_freinage = models.DecimalField(
         max_digits=6, decimal_places=2, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    background = models.CharField(max_length=50, default='default_background')

    def __str__(self):
        return f"Réglage de {self.user} pour {self.car}"


class Like(models.Model):
    reglage = models.ForeignKey(
        Reglage, on_delete=models.CASCADE, related_name="likes"
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = (
            "reglage",
            "user",
        )  # Ensure a user can only like a réglage once


class Trajet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="trajets")
    nom = models.CharField(max_length=100, help_text="Nom ou description du trajet")
    depart_lat = models.FloatField(help_text="Coordonnée Y en pixels du point de départ")
    depart_lng = models.FloatField(help_text="Coordonnée X en pixels du point de départ")
    etapes = models.JSONField(help_text="Liste des points intermédiaires sous forme de coordonnées pixels")
    arrivee_lat = models.FloatField(help_text="Coordonnée Y en pixels du point d'arrivée")
    arrivee_lng = models.FloatField(help_text="Coordonnée X en pixels du point d'arrivée")
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.user.username}"


# class MapElement(models.Model):
#     CATEGORY_CHOICES = [
#         ('solarCoins', 'Solar Coins'),
#         ('clan', 'Clan'),
#         ('reputation', 'Réputation'),
#         ('epave', 'Épave'),
#         ('epave2', 'Épave 2'),
#         ('concessionaire', 'Concessionnaire'),
#         ('station', 'Station'),
#         ('atelier', 'Atelier'),
#         ('rassemblement', 'Rassemblement'),
#     ]

#     district = models.DecimalField()  # Numéro de district (1 à 14)
#     category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)  # Catégorie principale
#     sub_category = models.CharField(max_length=50, blank=True, null=True)  # Sous-catégorie pour les concessionnaires
#     latitude = models.FloatField()  # Coordonnée latitude
#     longitude = models.FloatField()  # Coordonnée longitude

#     def __str__(self):
#         return f"{self.nom or 'Élément'} - {self.category} ({self.latitude}, {self.longitude})"
