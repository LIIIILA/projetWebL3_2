from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.utils.timezone import now

from datetime import datetime
datetime(2025, 1, 23, 10, 30)

from django.utils import timezone

field_name = models.DateTimeField(default=timezone.now)


from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class TimeSlot(models.Model):
    room = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_blocked = models.BooleanField(default=False)


class Box(models.Model):
    
    nom = models.CharField(max_length=100)
    capacity = models.IntegerField()
    site = models.ForeignKey('Site', on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('validated', 'Validated'),
        ('cancelled', 'Cancelled'),
    ]
    etudiant = models.ForeignKey('etudiant.Etudiant', on_delete=models.CASCADE, related_name='admin_reservations')  # Modifie le related_name
    box = models.ForeignKey('Box', on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = user = models.ForeignKey('administration.Administrateur', on_delete=models.CASCADE)

    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    start_time = models.TimeField()  
    end_time = models.DateTimeField(default=now)
    created_at = models.DateTimeField(auto_now_add=True)  # Champ pour la date de création
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"Reservation by {self.user.username} for {self.room.name} on {self.date}"


    
class Site(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

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
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Administrateur(AbstractUser):
    email = models.EmailField(unique=True)  # Utilise l'email comme identifiant
    username = None  # On supprime le champ username par défaut

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AdministrateurManager()

    # Champs 'groups' et 'user_permissions' avec 'related_name' unique
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='administrateurs_groups',  # Nom unique pour éviter le conflit
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='administrateurs_permissions',  # Nom unique pour éviter le conflit
        blank=True
    )

    class Meta:
        verbose_name = "Administrateur"
        verbose_name_plural = "Administrateurs"

