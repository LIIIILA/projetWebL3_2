from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db import models


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
    nom = models.CharField(max_length=100)
    capacity = models.IntegerField(default=1)  # Ajout d'une valeur par défaut
    opening_time = models.TimeField(default="09:00")
    closing_time = models.TimeField(default="19:00")

    def __str__(self):
        return self.nom


# Modèle Étudiant, basé sur AbstractUser
class Etudiant(AbstractUser):
    # Champs supplémentaires
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'etudiant_etudiant'  # Nom de la table dans la base de données

    def __str__(self):
        return self.username


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


# class Site(models.Model):
#     name = models.CharField(max_length=100, null=True, blank=True, default="Nom par défaut")

#     def __str__(self):
#         return self.name