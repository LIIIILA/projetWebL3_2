from django.contrib.auth.backends import BaseBackend
from etudiant.models import Etudiant

class EtudiantBackend(BaseBackend):
    def authenticate(self, request, username=None, **kwargs):
        print(f"Tentative d'authentification pour {username}")
        try:
            etudiant = Etudiant.objects.get(id_etudiant=username)
            print(f"Utilisateur trouvé : {etudiant}")
            return etudiant    
        except Etudiant.DoesNotExist:
            print("Aucun utilisateur correspondant.")
            return None

    def get_user(self, user_id):
        try:
            return Etudiant.objects.get(pk=user_id)
        except Etudiant.DoesNotExist:
            return None
