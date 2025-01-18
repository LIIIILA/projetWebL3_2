from django.db import models
from etudiant.models import Etudiant  
from datetime import timedelta
import datetime


class Salle(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    places = models.IntegerField()

    def __str__(self):
        return self.nom


class Box(models.Model):
    nom = models.CharField(max_length=100)  # Nom ou numéro de la box
    capacity = models.IntegerField(default=1)         # Capacité de la box
    salle = models.ForeignKey('reservation.Salle', on_delete=models.CASCADE)
  # Référence en chaîne
    opening_time = models.TimeField(default="09:00")  # Heure d'ouverture (par défaut 9h)
    closing_time = models.TimeField(default="19:00")  # Heure de fermeture (par défaut 19h)    

    def __str__(self):
        return self.nom



# Modèle Reservation
class Reservation(models.Model):
    id_etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)  # Utilisateur qui réserve
    box = models.ForeignKey(Box, on_delete=models.CASCADE, related_name="reservations")  # Box réservée
    start_time = models.TimeField()  # Heure de début
    end_time = models.TimeField()    # Heure de fin    
    date = models.DateField(default=datetime.date.today)
    
    def __str__(self):
        return f"Reservation: {self.id_etudiant} - Box: {self.box.nom} du {self.date} de {self.start_time} à {self.end_time}"


# Modèle Site
class Site(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.name


# Modèle PlageHoraire
class plageHoraire(models.Model):
    site = models.ForeignKey('Site', on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


