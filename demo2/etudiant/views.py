

from django.shortcuts import render, get_object_or_404
from .models import Salle
from .forms import ReservationForm


from django.shortcuts import render, get_object_or_404
from .models import Salle
from .forms import ReservationForm

import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .forms import LoginForm
from django.http import HttpResponse


def login(request):
    # Logique de la vue (par exemple, rendre un formulaire de connexion)
    return render(request, 'etudiant/login.html')

def login_view(request):
    return render(request, 'login.html')

def connexion(request):
    # Logique de la vue (par exemple, rendre un formulaire de connexion)
    return render(request, 'etudiant/connexion.html')

def index(request):
    return render(request, 'etudiant/index.html')

# Fonction pour générer un code de vérification
def generate_verification_code():
    return random.randint(100000, 999999)

def historique(request):
    return render(request, 'historique.html')

# def disponibilites(request):
#     salles = Salle.objects.prefetch_related('boxes')
#     return render(request, 'etudiant/disponibilites.html', {'disponibilites': disponibilites})

# def disponibilites_view(request):
#     salles = Salle.objects.all()
#     disponibilites = Disponibilite.objects.all()

#     # Application des filtres si présents dans la requête
#     if 'salle' in request.GET:
#         salles = salles.filter(id=request.GET['salle'])
#     if 'date' in request.GET:
#         disponibilites = disponibilites.filter(jour=request.GET['date'])

#     context = {
#         'salles': salles,
#         'disponibilites': disponibilites
#     }
#     return render(request, 'disponibilites.html', context)
def disponibilites(request):
    salles = Salle.objects.all()
    context = {
        'salles': salles,
    }
    return render(request, 'etudiant/disponibilites.html', context)

def reserver_box(request):
    # Logique pour gérer les réservations
    if request.method == "POST":
        # Traitement du formulaire
        pass
    return render(request, 'etudiant/reserver_box.html')

# Vue de connexion
# Stocke temporairement les codes envoyés (en production, utilisez un modèle ou un cache)
verification_codes = {}

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        code = request.POST.get("code")

        if not code:  # Si aucun code, envoyer un nouveau code
            verification_code = str(random.randint(100000, 999999))
            verification_codes[email] = verification_code

            send_mail(
                'Votre code de vérification',
                f'Votre code est : {verification_code}',
                'ton.email@example.com',
                [email],
                fail_silently=False,
            )
            return HttpResponse("Code envoyé à votre adresse email.")
        # else:
        #     if email in verification_codes and verification_codes[email] == code:
        #         return HttpResponse("Connexion réussie !")
        #     else:
        #         return HttpResponse("Code incorrect, veuillez réessayer.")
        else:  # Si un code est saisi, on le vérifie
            if 'verification_code' in request.session and str(request.session['verification_code']) == code:
                messages.success(request, "Connexion réussie !")
                return redirect('etudiant/login_etudiant.html')  # Rediriger l'utilisateur vers la page d'accueil ou autre
            else:
                messages.error(request, "Code incorrect, veuillez réessayer.")
                return redirect('login_etudiant.html')  # Redirige à la page de login pour réessayer

    return render(request, "etudiant/login.html")

def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        # Comparer le code saisi avec celui enregistré dans la session
        if code and int(code) == request.session.get('verification_code'):
            # Connexion réussie, on pourrait authentifier l'utilisateur ici
            messages.success(request, "Connexion réussie !")
            return redirect('etudiant/login_etudiant.html')  # Rediriger vers la page d'accueil ou une page protégée
        else:
            messages.error(request, "Code incorrect. Essayez à nouveau.")

    return render(request, 'etudiant/verify_code.html')


def send_test_email(request):
    send_mail(
        'Test Subject',
        'This is a test email.',
        'ton.email@kurl.com',  # L'adresse email de l'expéditeur
        ['destinataire@example.com'],  # L'adresse email du destinataire
        fail_silently=False,
    )
    return HttpResponse("Test email has been sent!")

def envoyer_code_verification(request):
    # Générer un code de vérification
    verification_code = generate_verification_code()

    # Envoyer le code par e-mail
    subject = "Votre code de vérification"
    message = f"Votre code de vérification est : {verification_code}"
    from_email = 'votre.email@gmail.com'
    recipient_list = ['utilisateur@example.com']  # À remplacer par l'adresse e-mail de l'utilisateur

    send_mail(subject, message, from_email, recipient_list)

    # Afficher un message de confirmation ou rediriger
    return render(request, 'confirmation.html', {'message': 'Code envoyé!'})

def send_verification_email(request):
    if request.method == "POST":
        identifier = request.POST.get('identifier')
        if len(identifier) == 8 and identifier.isdigit():  # Vérifie si l'identifiant est valide
            email = f"{identifier}@parisnanterre.fr"
            
            # Génère un code de vérification aléatoire
            verification_code = random.randint(1000, 9999)
            
            # Envoie l'email avec le code de vérification
            subject = "Code de Vérification"
            message = f"Votre code de vérification est : {verification_code}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            send_mail(subject, message, from_email, recipient_list)
            
            return HttpResponse("Code envoyé à votre adresse e-mail.")
        else:
            return HttpResponse("Identifiant invalide. Veuillez entrer un identifiant de 8 chiffres.")
    return HttpResponse("Méthode POST requise.")
