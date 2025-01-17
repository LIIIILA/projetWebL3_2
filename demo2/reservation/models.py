from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User



# Modèle Salle
class Salle(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    salle = models.IntegerField()
    places = models.IntegerField()
    heure_debut = models.TimeField(default="08:30")
    heure_fin = models.TimeField(default="20:30")
    duree_creneau = models.DurationField(default=timedelta(minutes=15))

    def __str__(self):
        return self.nom

    def clean(self):
        # Validation : heure_debut doit précéder heure_fin
        if self.heure_debut >= self.heure_fin:
            raise ValidationError("L'heure de début doit être avant l'heure de fin.")

    class Meta:
        verbose_name = "Salle"
        verbose_name_plural = "Salles"


# Modèle Box (lié à une Salle)
class Box(models.Model):
    numero = models.CharField(max_length=50)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, related_name="boxes")
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"Box {self.numero} ({'Disponible' if self.disponible else 'Occupé'})"


# Modèle Étudiant, basé sur AbstractUser
class Etudiant(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numero_etudiant = models.CharField(max_length=8, unique=True)

    class Meta:
        db_table = 'etudiant_etudiant'

    def __str__(self):
        return self.numero_etudiant


# Modèle Reservation
class Reservation(models.Model):
    salle = models.ForeignKey(
        'reservation.Salle',
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    utilisateur = models.ForeignKey(
        Etudiant,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    date = models.DateTimeField()

    def __str__(self):
        return f"Réservation de {self.salle.nom} le {self.date}"



class Site(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()

    def __str__(self):
        return self.nom

class plageHoraire(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"
