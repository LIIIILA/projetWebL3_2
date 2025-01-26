# from django.shortcuts import render

# # Create your views here.
# from django.shortcuts import render
# from reservation.models import Reservation

# def administration_index(request):
#     reservations = Reservation.objects.all()
#     return render(request, 'administration/administration_index.html', {'reservations': reservations})
from django.shortcuts import render, get_object_or_404, redirect
from reservation.models import Box,Site,Reservation, plageHoraire, Etudiant
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .forms import ReservationForm
from django.utils import timezone
from django.utils.timezone import now
from datetime import datetime

# @login_required
# def admin_dashboard(request):
#     # Récupérer toutes les réservations
#     reservations = Reservation.objects.all()

#     # Obtenir l'heure et la date actuelles
#     now_time = now()

#     # Filtrer les réservations passées
#     reservations_passees = reservations.filter(
#         date__lt=now_time.date()
#     ) | reservations.filter(
#         date=now_time.date(),
#         end_time__lt=now_time.time()
#     )
#     reservations_passees = reservations_passees.order_by('-date', '-end_time')

#     # Filtrer les réservations futures
#     reservations_futures = reservations.filter(
#         date__gt=now_time.date()
#     ) | reservations.filter(
#         date=now_time.date(),
#         start_time__gte=now_time.time()
#     )
#     reservations_futures = reservations_futures.order_by('date', 'start_time')

#     return render(request, 'administration/index_admin.html', {
#         'reservations_passees': reservations_passees,
#         'reservations_futures': reservations_futures,
#     })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm
from reservation.models import Box, Site, Etudiant, Reservation
from django.utils import timezone
from django.contrib.auth.models import User
from reservation.views import genration_horaires, get_sites, validation_datetime  # Assurez-vous que vos utils sont correctement importés

@login_required
def admin_dashboard(request):
    # Obtenir les boxes, étudiants, et réservations
    boxes = Box.objects.all()
    etudiants = Etudiant.objects.all()
    reservations = Reservation.objects.all()

    # Gestion des réservations passées et futures
    current_time = now()
    reservations_futures = reservations.filter(date__gte=current_time.date(), start_time__gte=current_time.time())
    reservations_passees = reservations.filter(date__lt=current_time.date())

    # Formulaire de réservation
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.admin = True  # Indique que l'admin fait la réservation
            reservation.save()
            return redirect('index_admin')
    else:
        form = ReservationForm()

    return render(request, 'administration/index_admin.html', {
        'boxes': boxes,
        'etudiants': etudiants,
        'reservations_futures': reservations_futures,
        'reservations_passees': reservations_passees,
        'form': form,
    })


@login_required
def modifier_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == "POST":
        reservation.date = request.POST['date']
        reservation.heure_debut = request.POST['start_time']
        reservation.heure_fin = request.POST['end_time']
        reservation.save()
        return redirect('admin_dashboard')
    return render(request, 'reservation/modifier_reservation.html', {'reservation': reservation})

# def annuler_reservation(request, id):
#     reservation = get_object_or_404(Reservation, id=id)
#     if request.method == 'POST':
#         reservation.delete()
#         # Redirige vers le tableau de bord après annulation
#         return redirect('admin_dashboard')  # Assurez-vous que le nom est correct ici
#     return render(request, 'administration/confirmation_annulation.html', {
#         'reservation': reservation
#     })

@login_required
def annuler_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    
    if request.method == 'POST':
        try:
            reservation.delete()
            messages.success(request, "La réservation a été annulée avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'annulation de la réservation : {str(e)}")
        return redirect('admin_dashboard')  # Rediriger vers le tableau de bord après l'annulation
    
    return render(request, 'administration/confirmation_annulation.html', {
        'reservation': reservation
    })

@login_required
def historique_reservations(request):
    site = Site.objects.all()
    historique = None
    salle_selectionnee = None
    if request.method == "POST":
        salle_id = request.POST['salle_id']
        salle_selectionnee = get_object_or_404(Site, id=salle_id)
        historique = Reservation.objects.filter(salle=salle_selectionnee).order_by('date', 'heure_debut')
    return render(request, 'reservation/admin_dashboard.html', {
        'site': Site,
        'historique': historique,
        'salle_selectionnee': salle_selectionnee,
    })


@login_required
def test_view(request):
    return render(request, 'administration/test.html')

def modifier_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('index_admin')  # Redirigez vers une page appropriée
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'administration/modifier_reservation.html', {'form': form})

# def historique_reservations(request):
#     etudiant_id = request.GET.get('etudiant_id')
    
#     if etudiant_id:
#         etudiant = get_object_or_404(Etudiant, id=etudiant_id)
#         # Filtrer les réservations passées et futures
#         reservations_passees = Reservation.objects.filter(etudiant=etudiant, date__lt=timezone.now())
#         reservations_futures = Reservation.objects.filter(etudiant=etudiant, date__gte=timezone.now())
#     else:
#         # Si aucun étudiant n'est sélectionné, on peut laisser les listes vides
#         reservations_passees = []
#         reservations_futures = []
    
#     return render(request, 'administration/index_admin.html', {
#         'reservations_passees': reservations_passees,
#         'reservations_futures': reservations_futures,
#         'etudiant': etudiant if etudiant_id else None
#     })
def historique_reservations(request):
    etudiants = Etudiant.objects.all()
    boxes = Box.objects.all()  # Récupérer les boxes

    # Récupérer les valeurs des filtres
    etudiant_id = request.GET.get('etudiant_id')
    box_id = request.GET.get('box_id')
    date = request.GET.get('date')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    # Filtrer les réservations
    reservations = Reservation.objects.all()
    if etudiant_id:
        reservations = reservations.filter(etudiant_id=etudiant_id)
    if box_id:
        reservations = reservations.filter(box_id=box_id)
    if date:
        reservations = reservations.filter(date=date)
    if start_time:
        reservations = reservations.filter(heure_debut__gte=start_time)
    if end_time:
        reservations = reservations.filter(heure_fin__lte=end_time)

    # Renvoyer les résultats au template
    return render(request, 'historique_reservations.html', {
        'etudiants': etudiants,
        'boxes': boxes,
        'reservations': reservations,
    })

@login_required
def admin_reservations(request):
    # Récupérer tous les étudiants et les boxes
    etudiants = Etudiant.objects.all()
    boxes = Box.objects.all()

    # Récupérer les valeurs des filtres depuis les paramètres GET
    etudiant_id = request.GET.get('etudiant_id', None)
    box_id = request.GET.get('box_id', None)
    date = request.GET.get('date', None)
    start_time = request.GET.get('start_time', None)
    end_time = request.GET.get('end_time', None)

    # Appliquer les filtres sur les réservations
    reservations_futures = Reservation.objects.filter(date__gte=datetime.today()).order_by('date', 'start_time')
    reservations_passees = Reservation.objects.filter(date__lt=datetime.today()).order_by('-date', '-start_time')

    if etudiant_id:
        reservations_futures = reservations_futures.filter(etudiant_id=etudiant_id)
        reservations_passees = reservations_passees.filter(etudiant_id=etudiant_id)
    
    if box_id:
        reservations_futures = reservations_futures.filter(box_id=box_id)
        reservations_passees = reservations_passees.filter(box_id=box_id)

    if date:
        reservations_futures = reservations_futures.filter(date=date)
        reservations_passees = reservations_passees.filter(date=date)

    if start_time:
        reservations_futures = reservations_futures.filter(start_time__gte=start_time)
        reservations_passees = reservations_passees.filter(start_time__gte=start_time)

    if end_time:
        reservations_futures = reservations_futures.filter(end_time__lte=end_time)
        reservations_passees = reservations_passees.filter(end_time__lte=end_time)

    # Rendre la page avec les résultats filtrés
    return render(request, 'administration/index_admin.html', {
        'etudiants': etudiants,
        'boxes': boxes,
        'reservations_futures': reservations_futures,
        'reservations_passees': reservations_passees,
        'etudiant_id': etudiant_id,
        'box_id': box_id,
        'date': date,
        'start_time': start_time,
        'end_time': end_time
    })

def reserver_admin(request):
    if request.method == 'POST':
        etudiant_id = request.POST.get('etudiant')
        box_id = request.POST.get('box')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if not etudiant_id or not box_id or not date or not start_time or not end_time:
            print("Erreur: Un ou plusieurs champs sont vides.")
            return redirect('admin_dashboard')

        box = Box.objects.get(id=box_id)
        etudiant = None if etudiant_id == "" else User.objects.get(id=etudiant_id)

        print(f"Box: {box}, Etudiant: {etudiant}, Admin: {request.user}")

        reservation = Reservation(
            box=box,
            start_time=start_time,
            end_time=end_time,
            date=date,
            etudiant=etudiant,
            id_admin=request.user
        )
        reservation.save()
        print(f"Réservation créée avec succès : {reservation}")
        return redirect('index_admin')

    return render(request, 'administration/reservation_admin.html')

def reservation_admin(request):
    # Générer les horaires possibles
    hours = genration_horaires()
    sites = get_sites()
    
    if request.method == 'POST':
        site_id = request.POST.get('site_id')  # ID du site sélectionné
        date = request.POST.get('date')        # Date choisie
        start_time = request.POST.get('start_time')  # Heure de début
        end_time = request.POST.get('end_time')      # Heure de fin

        # Validation des dates et heures
        is_valid, *validation_result = validation_datetime(date, start_time, end_time)
        print(f"Validation result index: {is_valid}, {validation_result}")  # Log pour déboguer

        if not is_valid:
            return render(request, 'reservation/disponibilite_boxes.html', {
                'sites': sites,
                'hours': hours,
                'error': validation_result[0],  # Message d'erreur retourné
            })
        else:
            # Si la validation est réussie, extraire les objets datetime de la validation
            start_datetime, end_datetime = validation_result[0], validation_result[1]  # Extraction correcte des objets datetime

            print(f"def index : Start datetime: {start_datetime}, End datetime: {end_datetime}")  # Log pour vérifier les objets datetime

            return redirect('disponibilite_boxes', site_id=site_id, date=date, start_time=start_time, end_time=end_time)

    # Si ce n'est pas une requête POST, afficher le formulaire
    return render(request, 'administration/page_reservation.html', {
        'sites': sites,
        'hours': hours,
    })

def disponibilite_boxes(request, site_id, date, start_time, end_time):
    hours = genration_horaires()
    sites = get_sites()

    # Convertir les chaînes en objets datetime
    try:
        start_datetime = datetime.strptime(f"{date} {start_time}", "%d-%m-%Y %H:%M")
        end_datetime = datetime.strptime(f"{date} {end_time}", "%d-%m-%Y %H:%M")
    except ValueError:
        return render(request, 'reservation/disponibilite_boxes.html', {
            'sites': sites,
            'hours': hours,
            'error': "Format de date ou d'heure invalide.",  # Message d'erreur
        })


    # Log de validation réussi
    print(f"Start datetime: {start_datetime}, End datetime: {end_datetime}")

    # Filtrer les boxes ouvertes dans la plage horaire demandée
    all_boxes = Box.objects.filter(
        site_id=site_id,
        opening_time__lte=start_datetime.time(),  # Comparer avec l'heure d'ouverture
        closing_time__gte=end_datetime.time()   # Comparer avec l'heure de fermeture
    )
    
    print(f"All boxes: {all_boxes}")  # Log pour vérifier les boxes récupérées

    # Filtrer les réservations qui chevauchent la plage horaire
    overlapping_reservations = Reservation.objects.filter(
        box__site_id=site_id,
        date=start_datetime.date(),  # Filtrer par la date
        start_time__lt=end_datetime.time(),  # Réservations qui commencent avant l'heure de fin
        end_time__gt=start_datetime.time()   # Réservations qui se terminent après l'heure de début
    ).values_list('box_id', 'start_time', 'end_time')

    #.values_list('box_id', flat=True)
    
    print(f"Overlapping reservations: {overlapping_reservations}")  # Log pour vérifier les réservations qui chevauchent

    reserved_timeslots = []

    # Ajouter tous les créneaux réservés pour les boxes
    for reservation in overlapping_reservations:
        reserved_timeslots.append({
            'box_id': reservation[0],
            'start_time': reservation[1],
            'end_time': reservation[2]
        })

    # Exclure les boxes réservées
    #available_boxes = all_boxes.exclude(id__in=overlapping_reservations)

    disponibilites = []

    for box in all_boxes:
        disponibilites_crenaux = []
        
        for hour in hours:
            if start_datetime.time() <= datetime.strptime(hour, "%H:%M").time() < end_datetime.time():
                is_reserved = False
                
                # Vérifier si ce créneau est réservé pour cette box
                for reservation in overlapping_reservations:
                    #if reservation[0] == box.id and reservation[1] == start_datetime.time() and reservation[2] == end_datetime.time():
                    if reservation[0] == box.id and reservation[1] <= datetime.strptime(hour, "%H:%M").time() < reservation[2]:
                        is_reserved = True
                        break
                #hour': reservation.start_time avt : hour': start_time
                disponibilites_crenaux.append({'hour': hour, 'is_reserved': is_reserved})
        
        disponibilites.append({'box': box, 'disponibilites_crenaux': disponibilites_crenaux})

    #print(f"Available boxes: {available_boxes}")  # Log pour vérifier les boxes disponibles

    
    return render(request, 'reservation/disponibilite_boxes.html', {
        #'boxes': available_boxes,
        'disponibilites': disponibilites,
        'start_time': start_datetime,
        'end_time': end_datetime,
        'site_id': site_id,
        'date':  start_datetime.strftime("%Y-%m-%d"),
        'hours': hours,
        'sites': sites
    })