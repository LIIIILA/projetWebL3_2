from django.db import models
from etudiant.models import Etudiant  
from datetime import timedelta
import datetime




# Create your models here.
class Box(models.Model):
    name = models.CharField(max_length=100)  # Nom ou numéro de la box
    capacity = models.IntegerField()         # Capacité de la box
    location = models.CharField(max_length=200)  # Localisation
    opening_time = models.TimeField(default="09:00")  # Heure d'ouverture (par défaut 9h)
    closing_time = models.TimeField(default="19:00")  # Heure de fermeture (par défaut 19h)    
    def __str__(self):
        return self.name



class Reservation(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)  # Utilisateur qui réserve
    box = models.ForeignKey(Box, on_delete=models.CASCADE)           # Box réservée
    start_time = models.DateTimeField()                              # Début de la réservation
    end_time = models.DateTimeField()                                # Fin de la réservation
    code = models.CharField(max_length=10, unique=True)              # Code unique pour vérifier
    
    
    
