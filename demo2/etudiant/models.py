from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.conf import settings
from django.apps import AppConfig


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


# Modèle Reservation
# Modèle Reservation
# Modèle Étudiant, basé sur AbstractUser
# Modèle Étudiant, basé sur AbstractUser
class Etudiant(AbstractUser):
    # Champs supplémentaires
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'etudiant_etudiant'  # Nom de la table dans la base de données

    def __str__(self):
        return self.username


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


# Modèle Reservation
class Reservation(models.Model):
    salle = models.ForeignKey(
        Salle,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    date = models.DateTimeField()
    utilisateur = models.ForeignKey(
        Etudiant,  # Remplacez CharField par une clé étrangère vers le modèle Etudiant
        on_delete=models.CASCADE,
        related_name='reservations'  # Lien entre l'utilisateur et ses réservations
    )

    def __str__(self):
        return f"Réservation de {self.salle.nom} le {self.date}"


