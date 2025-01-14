

from django.shortcuts import render, get_object_or_404
from .forms import ReservationForm

from django.contrib.auth import logout

import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .forms import LoginForm
from django.http import HttpResponse
from django.utils.dateparse import parse_date, parse_time


from .models import Reservation
from datetime import timedelta


def connexion(request):
    # Logique de la vue (par exemple, rendre un formulaire de connexion)
    return render(request, 'etudiant/connexion.html')



def index(request):
    return render(request, 'etudiant/index.html')

# Fonction pour générer un code de vérification
def generate_verification_code():
    return random.randint(100000, 999999)

def historique(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    salles = Salle.objects.all()  # Assurez-vous de récupérer les salles disponibles si nécessaire
    return render(request, 'etudiant/historique.html', {'reservations': reservations, 'salles': salles})


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

def generate_time_slots():
    # Démarrer à 08:30
    start_time = timedelta(hours=8, minutes=30)
    # Fin à 20:30
    end_time = timedelta(hours=20, minutes=30)

    time_slots = []

    current_time = start_time
    while current_time <= end_time:
        hour = (current_time.seconds // 3600)
        minute = (current_time.seconds // 60) % 60
        time_slots.append(f'{hour:02}:{minute:02}')
        current_time += timedelta(minutes=15)
    
    return time_slots


def reserver_box(request):
    if request.method == "POST":
        # Récupérer les données envoyées via le formulaire
        salle_id = request.POST.get("salle")  # ID de la salle sélectionnée
        box_id = request.POST.get("box")  # ID de la box sélectionnée
        date_str = request.POST.get("date")  # Date
        start_time_str = request.POST.get("start_time")  # Heure de départ
        end_time_str = request.POST.get("end_time")  # Heure de fin

        # Validation des données
        if not salle_id or not box_id or not date_str or not time_str:
            messages.error(request, "Tous les champs sont obligatoires.")
            return redirect('reserver_box')

        # Conversion de la date et de l'heure en objets datetime
        try:
            date = parse_date(date_str)
            start_time = parse_time(start_time_str)
            end_time = parse_time(end_time_str)
        except ValueError:
            messages.error(request, "La date ou l'heure saisie est incorrecte.")
            return redirect('reserver_box')
        
        if end_time <= start_time:
            messages.error(request, "L'heure de fin doit être après l'heure de départ.")
            return redirect('reserver_box')

        # Trouver la salle et la box correspondantes
        try:
            salle = Salle.objects.get(id=salle_id)
            box = Box.objects.get(id=box_id)
        except Salle.DoesNotExist or Box.DoesNotExist:
            messages.error(request, "Salle ou Box non trouvée.")
            return redirect('reserver_box')

        # Créer la réservation
        reservation = Reservation.objects.create(
            salle=salle,
            box=box,
            date=date,
            heure_debut=start_time,
            heure_fin=end_time,
            user=request.user
        )

        # Message de succès
        messages.success(request, "Votre réservation a été effectuée avec succès !")
        return redirect('historique')  # Ou rediriger vers une autre page, comme l'historique des réservations

    # Afficher le formulaire avec les données des salles et des boxes disponibles
    time_slots = generate_time_slots()

    salles = Salle.objects.all()
    boxes = Box.objects.all()  # Assurez-vous de filtrer en fonction de la salle sélectionnée si nécessaire
    return render(request, 'etudiant/reserver_box.html', {'salles': salles, 'boxes': boxes})

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

def custom_logout(request):
    if request.method == "POST":  # S'assurer que la déconnexion se fait via POST
        logout(request)
        return redirect('/')  # Redirection après déconnexion
    return redirect('/')  # Rediriger si méthode GET (ou afficher une page de confirmation)

