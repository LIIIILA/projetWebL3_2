from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta


# Create your models here.


class Etudiant(AbstractUser):
    # Vous pouvez ajouter des champs supplémentaires ici
    date_of_birth = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'etudiant_etudiant'  # Nom de la table dans la base de données
    def __str__(self):
        return self.username
    


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

class Box(models.Model):
    numero = models.CharField(max_length=50)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, related_name="boxes")
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"Box {self.numero} ({'Disponible' if self.disponible else 'Occupé'})"


