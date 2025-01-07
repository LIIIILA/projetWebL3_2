from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Etudiant(AbstractUser):
    # Vous pouvez ajouter des champs supplémentaires ici
    date_of_birth = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'etudiant_etudiant'  # Nom de la table dans la base de données
    def __str__(self):
        return self.username
