
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
import datetime
from reservation.models import Box


class Salle(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Reservation(models.Model):
    id_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="administration_reservations")
    box = models.ForeignKey(Box, on_delete=models.CASCADE, related_name="administration_reservations")
    start_time = models.TimeField()  # Heure de début
    end_time = models.TimeField()    # Heure de fin    
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"Reservation: {self.id_admin} - Box: {self.box.nom} du {self.date} de {self.start_time} à {self.end_time}"