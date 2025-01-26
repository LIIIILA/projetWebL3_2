# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from datetime import timedelta
# from django.core.exceptions import ValidationError
# from django.conf import settings
# from django.apps import AppConfig



# class Etudiant(AbstractUser):
#     # Champs supplémentaires
#     date_of_birth = models.DateField(null=True, blank=True)

#     class Meta:
#         db_table = 'etudiant_etudiant'  # Nom de la table dans la base de données

#     def __str__(self):
#         return self.username
    
    
# class Reservation(models.Model):
#     # Reportez l'importation du modèle Site ici
#     site = models.ForeignKey(
#         'reservation.Site',  # Utilisez la référence de modèle sous forme de chaîne de caractères pour éviter l'importation circulaire
#         on_delete=models.CASCADE,swappable=False,
#     )
#     date = models.DateTimeField()
#     utilisateur = models.ForeignKey(
#         Etudiant,
#         on_delete=models.CASCADE,
#         related_name='reservations'
#     )

#     def __str__(self):
#         return f"Réservation du site {self.site.name} le {self.date}"

# etudiant/models.py

from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.conf import settings
from django.apps import AppConfig
from django.contrib.auth.models import User



from django.db import models

class Etudiant(AbstractUser):
    # Champs supplémentaires
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'etudiant_etudiant'  # Nom de la table dans la base de données

    def __str__(self):
        return self.username
