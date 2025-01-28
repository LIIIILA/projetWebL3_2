from django.db import models
from django.contrib.auth.models import AbstractUser

class Etudiant(AbstractUser):
    id_etudiant = models.CharField(max_length=20, unique=True, primary_key=True,verbose_name="Identifiant étudiant")  
    email = models.EmailField(unique=True,verbose_name="Adresse email")
    is_blacklisted = models.BooleanField(default=False, verbose_name="BLacklisté")
    password = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'id_etudiant'
    REQUIRED_FIELDS = ['id_etudiant']  # Indique que 'id_etudiant' est requis lors de la création d'un utilisateur
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='etudiant_set',  # Nom unique pour éviter le conflit
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='etudiant_permissions',  # Nom unique pour éviter le conflit
        blank=True
    )

    class Meta:
        db_table = 'etudiant_etudiant'
        verbose_name = "Étudiant" 
        verbose_name_plural = "Étudiants"  

    
    def __str__(self):
        return f"{self.id_etudiant} - {self.email}"

