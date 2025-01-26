
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
import datetime
from reservation.models import Box, Site, Reservation, plageHoraire,Etudiant  # Corrigez si nécessaire
from datetime import time



# class Salle(models.Model):
#     nom = models.CharField(max_length=100)

#     def __str__(self):
#         return self.nom

class Reservation(models.Model):
    id_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="administration_reservations")
#     box = models.ForeignKey(Box, on_delete=models.CASCADE, related_name="administration_reservations")
#     start_time = models.TimeField()  # Heure de début
#     end_time = models.TimeField()    # Heure de fin
#     date = models.DateField(default=datetime.date.today)

#     def __str__(self):
#         return f"Reservation: {self.id_admin} - Box: {self.box.nom} du {self.date} de {self.start_time} à {self.end_time}"

class Box(models.Model):
    # Définition de la liste des choix pour les horaires
    TIME_CHOICES = [
        (time(9, 0), '09:00'),
        (time(10, 0), '10:00'),
        (time(11, 0), '11:00'),
        (time(12, 0), '12:00'),
        (time(13, 0), '13:00'),
        (time(14, 0), '14:00'),
        (time(15, 0), '15:00'),
        (time(16, 0), '16:00'),
        (time(17, 0), '17:00'),
        (time(18, 0), '18:00'),
    ]
