from django.db import models
from etudiant.models import Etudiant  
from datetime import datetime
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.utils import timezone


class Box(models.Model):
    nom = models.CharField(max_length=100)  
    capacity = models.IntegerField()         
    site = models.ForeignKey('Site', on_delete=models.CASCADE)  
    opening_time = models.TimeField(default="08:30")  
    closing_time = models.TimeField(default="18:45")      
    def __str__(self):
        return self.nom



class Reservation(models.Model):
    id_etudiant = models.ForeignKey('etudiant.Etudiant', on_delete=models.CASCADE)  # Utilisateur qui réserve
    box = models.ForeignKey('Box', on_delete=models.CASCADE,related_name="reservations")           # Box réservée
    start_time = models.TimeField()  # Heure de début
    end_time = models.TimeField()    # Heure de fin    
    date = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return f"Reservation: {self.id_etudiant} - Box: {self.box.nom}  du {self.date} de {self.start_time} à {self.end_time}"
    
    @staticmethod   
    def historique(etudiant):
        now = datetime.now()  # Date et heure actuelles
        
        # Filtrer les réservations futures
        reservations_futures = etudiant.reservation_set.filter(
            date__gt=now.date()  # Réservations après la date d'aujourd'hui
        ).order_by('date', 'start_time')
        
        # Réservations du jour mais dont l'heure est encore dans le futur
        reservations_futures_du_jour = etudiant.reservation_set.filter(
            date=now.date(), start_time__gte=now.time()
        ).order_by('start_time')

        # Combiner les futures réservations
        reservations_futures = reservations_futures | reservations_futures_du_jour

        # Filtrer les réservations passées
        reservations_passees = etudiant.reservation_set.filter(
            date__lt=now.date()  # Réservations avant aujourd'hui
        ).order_by('-date', '-start_time')
        
        # Réservations du jour mais dont l'heure est déjà passée
        reservations_passees_du_jour = etudiant.reservation_set.filter(
            date=now.date(), end_time__lt=now.time()
        ).order_by('-end_time')

        # Combiner les passées réservations
        reservations_passees = reservations_passees | reservations_passees_du_jour

        return reservations_futures, reservations_passees
    
    def est_autorise(self, user):
        """Vérifie si l'utilisateur peut modifier ou annuler la réservation."""
        if self.id_etudiant != user:
            raise PermissionDenied("Vous n'êtes pas autorisé à effectuer cette action sur cette réservation.")
        now = datetime.now()
        reservation_datetime = datetime.combine(self.date, self.start_time)
        if reservation_datetime <= now:
            raise PermissionDenied("La réservation est déjà passée ou en cours.")
        return True

    def annuler(self, user):
        """Annule une réservation après avoir vérifié les permissions."""
        self.est_autorise(user)  # Vérification des droits
        self.delete()

    def modifier(self, user, nouvelle_date, nouvel_start_time, nouvel_end_time):
        """Modifie une réservation après avoir vérifié les permissions."""
        self.est_autorise(user)  

        self.id_etudiant=user.id_etudiant
        self.date = nouvelle_date
        self.start_time = nouvel_start_time
        self.end_time = nouvel_end_time
        
        self.save()
    
    # def save(self, *args, **kwargs):
    #     self.quota_journaliere()
    #     self.delais_reservation()
    #     super().save(*args, **kwargs)

    # def quota_journaliere(self):
    #     """Vérifie si l'étudiant a atteint le quota de 3 réservations par jour."""
    #     today_reservations = Reservation.objects.filter(
    #         etudiant=self.etudiant,
    #         date=self.date  # Vérifie les réservations pour cette journée
    #     )
        
    #     if today_reservations.count() >= 4:
    #         raise ValidationError("Vous avez atteint la limite de 3 réservations pour aujourd'hui.")

    # def delais_reservation(self):
    #     """Vérifie si 24 heures se sont écoulées depuis la dernière réservation."""
    #     last_reservation = Reservation.objects.filter(etudiant=self.etudiant).order_by('-date', '-start_time').first()
        
    #     if last_reservation:
    #         last_reservation_time = timezone.make_aware(datetime.combine(last_reservation.date, last_reservation.end_time))
    #         time_difference = timezone.now() - last_reservation_time
    #         if time_difference < timedelta(hours=24):
    #             raise ValidationError("Vous devez attendre 24 heures avant de pouvoir effectuer une nouvelle réservation.")
    
    
class Site(models.Model):
    nom=models.CharField(max_length=100)
    def __str__(self):
        return self.nom
    

