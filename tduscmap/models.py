
from django.db import models

from authentication.models import CustomUser


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='favorites')
    lat = models.FloatField()  # Latitude
    lng = models.FloatField()  # Longitude
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s favorite at ({self.lat}, {self.lng})"
