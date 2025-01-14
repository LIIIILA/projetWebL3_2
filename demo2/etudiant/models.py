# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from datetime import timedelta
# from django.contrib.auth.models import User


# # Create your models here.


# class Etudiant(AbstractUser):
#     # Vous pouvez ajouter des champs supplémentaires ici
#     date_of_birth = models.DateField(null=True, blank=True)
#     class Meta:
#         db_table = 'etudiant_etudiant'  # Nom de la table dans la base de données
#     def __str__(self):
#         return self.username
    


# class Salle(models.Model):
#     nom = models.CharField(max_length=100)
#     description = models.TextField()
#     salle = models.IntegerField() 
#     places = models.IntegerField()
#     heure_debut = models.TimeField(default="08:30")
#     heure_fin = models.TimeField(default="20:30")
#     duree_creneau = models.DurationField(default=timedelta(minutes=15))

#     def __str__(self):
#         return self.nom

# class Box(models.Model):
#     numero = models.CharField(max_length=50)
#     salle = models.ForeignKey(Salle, on_delete=models.CASCADE, related_name="boxes")
#     disponible = models.BooleanField(default=True)

#     def __str__(self):
#         return f"Box {self.numero} ({'Disponible' if self.disponible else 'Occupé'})"

# class Reservation(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     room = models.CharField(max_length=100)  # Exemple de champ pour la salle
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'Reservation de {self.room} pour {self.user.username}'

from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import User

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


# Modèle Box (lié à une Salle)
class Box(models.Model):
    numero = models.CharField(max_length=50)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, related_name="boxes")
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"Box {self.numero} ({'Disponible' if self.disponible else 'Occupé'})"


# Modèle Reservation
class Reservation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations"  # Ajout d'un related_name pour éviter les conflits
    )
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)  # Utilisation de ForeignKey pour la salle
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Réservation de {self.salle.nom} pour {self.user.username}"

    def clean(self):
        # Validation : start_time doit précéder end_time
        if self.start_time >= self.end_time:
            raise ValidationError("L'heure de début doit être avant l'heure de fin.")

