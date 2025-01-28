from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class AdministrateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.update({
            'is_staff': True,
            'is_superuser': True
        })
        return self.create_user(email, password, **extra_fields)


class Administrateur(AbstractUser):
    email = models.EmailField(unique=True)  # Utilise l'email comme identifiant
    username = None  # On supprime le champ `username` par défaut

    USERNAME_FIELD = 'email'  # L'email sera utilisé pour l'authentification
    REQUIRED_FIELDS = []  # Aucun champ supplémentaire requis

    # Ajout des groupes avec un `related_name` unique pour éviter le conflit
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='administrateurs',  # Nom unique pour éviter le conflit
        blank=True
    )
    
    # Ajout des permissions avec un `related_name` unique pour éviter le conflit
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='administrateur_permissions',  # Nom unique pour éviter le conflit
        blank=True
    )
    
    objects = AdministrateurManager()  # Utilise le gestionnaire personnalisé

    class Meta:
        verbose_name = "Administrateur"
        verbose_name_plural = "Administrateurs"

    def __str__(self):
        return self.email




from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
import datetime
from reservation.models import Box, Site, Reservation,Etudiant  # Corrigez si nécessaire
from datetime import time



class Reservation(models.Model):
    id_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="administration_reservations")

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