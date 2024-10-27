
from django.db import models
from django.utils import timezone
from authentication.models import CustomUser


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='favorites')
    lat = models.FloatField()  # Latitude
    lng = models.FloatField()  # Longitude
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s favorite at ({self.lat}, {self.lng})"


class Car(models.Model):
    MARQUES = [
        ('Abarth', 'Abarth'),
        ('AC', 'AC'),
        ('Alpha Romeo', 'Alpha Romeo'),
        ('Alpine', 'Alpine'),
        ('Aston Martin', 'Aston Martin'),
        ('Audi', 'Audi'),
        ('Bentley', 'Bentley'),
        ('BMW', 'BMW'),
        ('Bugatti', 'Bugatti'),
        ('Caterham', 'Caterham'),
        ('Chevrolet', 'Chevrolet'),
        ('Citroen', 'Citroen'),
        ('Dodge', 'Dodge'),
        ('Ferrari', 'Ferrari'),
        ('Ford', 'Ford'),
        ('Jaguar', 'Jaguar'),
        ('Koenlgsegg', 'Koenlgsegg'),
        ('Lamborghini', 'Lamborghini'),
        ('Lancia', 'Lancia'),
        ('Lotus', 'Lotus'),
        ('McLaren', 'McLaren'),
        ('Mercedes-AMG', 'Mercedes-AMG'),
        ('Mercedes-Benz', 'Mercedes-Benz'),
        ('Mini', 'Mini'),
        ('Nissan', 'Nissan'),
        ('Porshe', 'Porshe'),
        ('Shelby', 'Shelby'),
        ('Sientero', 'Sientero'),
        ('WMotors', 'WMotors'),
        ('Wolkwagen', 'Wolkswagen'),
    ]
    TRANSMISSIONS = [
        ('RWD', 'RWD'),
        ('FWD', 'FWD'),
        ('4WD', '4WD'),
    ]
    
    CATEGORIES = [
        ('A', 'Catégorie A'),
        ('B', 'Catégorie B'),
        ('C', 'Catégorie C'),
        ('D', 'Catégorie D'),
        ('E', 'Catégorie E'),
        ('F', 'Catégorie F'),
        ('G', 'Catégorie G'),
        ('H', 'Catégorie H'),
    ]
    
    RARETES = [
        ('légendaire', 'Légendaire'),
        ('épique', 'Épique'),
        ('rare', 'Rare'),
        ('commun', 'Commun'),
        ('peu commun', 'Peu commun'),
        (None, 'Aucune'),
    ]
    
    marque = models.CharField(max_length=50, choices=MARQUES)
    modele = models.CharField(max_length=50)
    annee = models.PositiveIntegerField()
    transmission = models.CharField(max_length=3, choices=TRANSMISSIONS)
    
    ip = models.PositiveIntegerField()
    categorie = models.CharField(max_length=1, choices=CATEGORIES)
    rarete = models.CharField(max_length=10, choices=RARETES, blank=True, null=True)
    prix_initial = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.annee})"


class CarPrice(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="historique_prix")
    prix = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.car.marque} {self.car.modele} - {self.date}: {self.prix}€"
