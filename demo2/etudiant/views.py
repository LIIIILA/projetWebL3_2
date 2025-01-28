

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout,login as auth_login,authenticate
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime,timedelta
from etudiant.models import Etudiant
from reservation.models import Site, Reservation
import random
from .models import Etudiant
from django.contrib.auth.decorators import login_required


def login(request):
    return render(request, 'etudiant/login.html')


@login_required(login_url='reservation_index')
def deconnexion(request):
    if request.method =="POST":  
        if 'details_reservation' in request.session:
            del request.session['details_reservation']
        logout(request)
        return render (request,'etudiant/deconnexion.html')
    return redirect('/') 


@login_required(login_url='login_view')
def profil(request):
    try:
        etudiant = Etudiant.objects.get(id_etudiant=request.user.id_etudiant)

        reservations_futures, reservations_passees = Reservation.historique(etudiant)

        return render(request, 'etudiant/profil.html', {
            'identifiant': etudiant.id_etudiant,
            'reservations_futures': reservations_futures,
            'reservations_passees': reservations_passees
        })

    except Etudiant.DoesNotExist:
        messages.error(request, "Vous devez être connecté en tant qu'étudiant pour accéder à cette page.")
        
        return redirect('login_view')


# Stocke temporairement les codes envoyés (en production, utilisez un modèle ou un cache)
verification_codes = {}

# Fonction utilitaire : envoyer un code de vérification
def envoyer_code_verification(email):
    verification_code = str(random.randint(100000, 999999))
    verification_codes[email] = {
        'code': verification_code,
        'timestamp': datetime.now(),
    }

    # Envoyer l'email avec le code
    send_mail(
        'Votre code de vérification',
        f'Votre code est : {verification_code}',
        'noreply@example.com',
        [f"{email}@parisnanterre.fr"],
        fail_silently=False,
    )
    return verification_code

# Fonction utilitaire : vérifier le code de vérification
def verifier_code(email, code):
    if email not in verification_codes:
        return False, "Aucun code de vérification trouvé. Veuillez demander un code."

    code_data = verification_codes[email]
    expiration_time = code_data['timestamp'] + timedelta(minutes=5)

    if datetime.now() > expiration_time:
        del verification_codes[email]
        return False, "Le code de vérification a expiré. Veuillez en demander un nouveau."

    if code_data['code'] != code:
        return False, "Code de vérification incorrect."

    del verification_codes[email]  # Supprimer le code après vérification réussie
    return True, None

# Fonction principale : Vue pour le login
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        code = request.POST.get("code")

        if not code:  # Étape 1 : Envoi du code de vérification
            if email and email.isdigit() and len(email) == 8:
                envoyer_code_verification(email)
                return render(request, "etudiant/login.html", {"email": email, "step": 2})
            else:
                messages.error(request, "L'identifiant doit contenir exactement 8 chiffres.")
                
                return render(request, "etudiant/login.html", {"step": 1})

        else:  
            success, error_message = verifier_code(email, code)
            if not success:
                messages.error(request, error_message)
                  
                return render(request, "etudiant/login.html", {"email": email, "step": 2})

            user, created = Etudiant.objects.get_or_create(
                id_etudiant=email,
                email=f"{email}@parisnanterre.fr",
                defaults={'is_active': True, 'is_blacklisted': False},
            )
            if created:
                print(f"Nouvel utilisateur créé : {user}")
            else:
                print("Utilisateur existant récupéré.")

            # Authentifier et connecter l'utilisateur
            user = authenticate(request, username=email)
            if user:
                auth_login(request, user)
                request.session.save()

                donnees_reservation = request.session.get('details_reservation')
                if donnees_reservation:
                    return redirect(request.GET.get('next', 'verification'))
                
                return redirect('profil')
            else:
                
                messages.error(request, "La connexion a échoué. Veuillez réessayer.")
                return redirect('login_view')

    return render(request, "etudiant/login.html", {"step": 1})

