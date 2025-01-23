from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.utils.timezone import now

from datetime import datetime
datetime(2025, 1, 23, 10, 30)

from django.utils import timezone

field_name = models.DateTimeField(default=timezone.now)


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # Modifiez les champs 'groups' et 'user_permissions' pour spécifier des 'related_name' uniques
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Nom unique pour éviter le conflit
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Nom unique pour éviter le conflit
        blank=True
    )

    def __str__(self):
        return self.username
    
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')  # Nom unique
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
