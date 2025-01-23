# from django.db import models 
# from datetime import timedelta
# import datetime




# # Create your models here.
# class Box(models.Model):
#     nom = models.CharField(max_length=100)  # Nom ou numéro de la box
#     capacity = models.IntegerField()         # Capacité de la box
#     site = models.ForeignKey('Site', on_delete=models.CASCADE)  
#     opening_time = models.TimeField(default="09:00")  # Heure d'ouverture (par défaut 9h)
#     closing_time = models.TimeField(default="19:00")  # Heure de fermeture (par défaut 19h)    
#     def _str_(self):
#         return self.nom

# class Reservation(models.Model):
#     id_etudiant = models.ForeignKey(
#         'etudiant.Etudiant',  # Utilisation de la chaîne pour éviter l'importation circulaire
#         on_delete=models.CASCADE, swappable=False,
#     )  
#     box = models.ForeignKey(Box, on_delete=models.CASCADE, related_name="reservations")
#     start_time = models.TimeField()
#     end_time = models.TimeField()    
#     date = models.DateField(default=datetime.date.today)

#     def __str__(self):
#         return f"Reservation: {self.id_etudiant} - Box: {self.box.nom} du {self.date} de {self.start_time} à {self.end_time}"

    
    
# class Site(models.Model):
#     nom=models.CharField(max_length=100)
#     def _str_(self):
#         return self.nom
    

# class plageHoraire(models.Model):
#     site = models.ForeignKey('Site', on_delete=models.CASCADE, null=True, blank=True)
#     start_time = models.TimeField()
#     end_time = models.TimeField()

#     def _str_(self):
#         return f"{self.start_time} - {self.end_time}"

# reservation/models.py
import datetime
from django.db import models
from etudiant.models import Etudiant  # Importation explicite pour éviter l'import circulaire

class Box(models.Model):
    nom = models.CharField(max_length=100)  # Nom ou numéro de la box
    capacity = models.IntegerField()         # Capacité de la box
    site = models.ForeignKey('Site', on_delete=models.CASCADE)  
    opening_time = models.TimeField(default="09:00")  # Heure d'ouverture (par défaut 9h)
    closing_time = models.TimeField(default="19:00")  # Heure de fermeture (par défaut 19h)    
    def __str__(self):
        return self.nom

class Reservation(models.Model):
    id_etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)  # Utilisateur qui réserve
    box = models.ForeignKey(Box, on_delete=models.CASCADE, related_name="reservations")           # Box réservée
    start_time = models.TimeField()  # Heure de début
    end_time = models.TimeField()    # Heure de fin    
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"Reservation: {self.id_etudiant} - Box: {self.box.nom} du {self.date} de {self.start_time} à {self.end_time}"

class Site(models.Model):
    nom = models.CharField(max_length=100)
    def __str__(self):
        return self.nom

class plageHoraire(models.Model):
    site = models.ForeignKey('Site', on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

class BoxReservation(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    user = models.CharField(max_length=100)  # Exemple : identifiant étudiant
    box_type = models.CharField(max_length=50, choices=[('Small', 'Petit'), ('Large', 'Grand')])

    def __str__(self):
        return f"Réservation de {self.user} - {self.date} de {self.start_time} à {self.end_time}"