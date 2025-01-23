from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings

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

class Timeslot(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.room.name}: {self.start_time} - {self.end_time}"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('validated', 'Validated'),
        ('cancelled', 'Cancelled'),
    ]
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')  # Nom unique
    date = models.DateField()
    timeslot = models.ForeignKey(Timeslot, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Reservation by {self.user.username} for {self.room.name} on {self.date}"