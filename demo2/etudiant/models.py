from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.conf import settings
from django.apps import AppConfig



class Etudiant(AbstractUser):
    # Champs supplémentaires
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'etudiant_etudiant'  # Nom de la table dans la base de données

    def __str__(self):
        return self.username

