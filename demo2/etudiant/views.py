import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .forms import LoginForm
from django.http import HttpResponse

def index(request):
    return render(request, 'etudiant/index.html')

# Fonction pour générer un code de vérification
def generate_verification_code():
    return random.randint(100000, 999999)

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
        else:
            if email in verification_codes and verification_codes[email] == code:
                return HttpResponse("Connexion réussie !")
            else:
                return HttpResponse("Code incorrect, veuillez réessayer.")

    return render(request, "etudiant/login.html")

def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        # Comparer le code saisi avec celui enregistré dans la session
        if code and int(code) == request.session.get('verification_code'):
            # Connexion réussie, on pourrait authentifier l'utilisateur ici
            messages.success(request, "Connexion réussie !")
            return redirect('home')  # Rediriger vers la page d'accueil ou une page protégée
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
