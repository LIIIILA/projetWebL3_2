
from django.shortcuts import redirect, render
from .models import Box, Reservation, Site
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import BoxReservationForm

def genration_horaires():
    hours = []
    start_time = datetime.strptime("08:30", "%H:%M")
    end_time = datetime.strptime("18:45", "%H:%M")

    current_time = start_time
    while current_time <= end_time:
        hours.append(current_time.strftime('%H:%M'))
        current_time += timedelta(minutes=15)
    
    return hours


def validation_datetime(date, start_time, end_time):  
    try:
        start_datetime = datetime.strptime(f"{date} {start_time}", "%d-%m-%Y %H:%M")
        end_datetime = datetime.strptime(f"{date} {end_time}", "%d-%m-%Y %H:%M")
    except ValueError:
        return False, 'Format de date ou d\'heure invalide.'
    
    if start_datetime >= end_datetime:
        return False, 'L\'heure de début doit être avant l\'heure de fin.'
    
    return True, start_datetime, end_datetime


def get_sites():
    return Site.objects.all()



def reservation_index(request):
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
    return render(request, 'reservation/index.html', {
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




def verification(request):
    if request.method == 'POST':
        box_id = request.POST.get('box_id')
        selected_hour = request.POST.get('selected_hour')
        date = request.POST.get('date')
        print(f"Date: {date}, Box ID: {box_id}, Selected Hour: {selected_hour}") 

        if not request.user.is_authenticated:
            request.session['reservation_data'] = {
                'box_id': box_id,
                'selected_hour': selected_hour,
                'date': date,
            }
            return redirect('identification')
        else:
            box = Box.objects.get(id=box_id)      
            start_time = datetime.strptime(selected_hour, '%H:%M')
            end_time = start_time + timedelta(minutes=15)

        return render(request, 'reservation/verification.html', {
            'message': 'Veuillez valider la réservation.',
            'box':box,
            'date':date,
            'start_time': start_time,
            'end_time': end_time,
            })
    
    

def identification(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)  # Formulaire avec les données soumises
        if form.is_valid():
            user = form.get_user()  # Récupère l'utilisateur validé
            login(request, user)  # Connecte l'utilisateur

            
            reservation_data = request.session.get('reservation_data')
            if reservation_data:
                return redirect('validation')

            return redirect('index_reservation')  # Sinon, redirige vers la page d'accueil
    else:
        form = AuthenticationForm()

    return render(request, 'reservation/login.html', {'form': form})

def validation(request):
    # Vérifie si les données de réservation existent dans la session
    reservation_data = request.session.get('reservation_data')

    # Si l'utilisateur est déjà connecté, les données doivent être récupérées même sans la session
    if not reservation_data and request.user.is_authenticated:
        # Si l'utilisateur est authentifié et qu'il n'y a pas de données dans la session, on récupère les données du formulaire (par exemple via un POST)
        box_id = request.POST.get('box_id')
        selected_hour = request.POST.get('selected_hour')
        date = request.POST.get('date')

        reservation_data = {
            'box_id': box_id,
            'selected_hour': selected_hour,
            'date': date
        }

    if not reservation_data:
        return redirect('reservation_index')  # Redirige si aucune donnée n'est trouvée

    # Récupère les données de la réservation
    box_id = reservation_data['box_id']
    selected_hour = reservation_data['selected_hour']
    date = reservation_data['date']

    print(f"Réservation confirmée : Box ID: {box_id}, Hour: {selected_hour}, Date: {date}")
    
    # Récupère les détails de la réservation
    box = Box.objects.get(id=box_id)
    start_time = datetime.strptime(selected_hour, '%H:%M')
    end_time = start_time + timedelta(minutes=15)

    # Sauvegarde de la réservation dans la base de données
    reservation = Reservation(
            box=box,
            id_etudiant=request.user,
            date=date,
            start_time=start_time,
            end_time=end_time
        )
    reservation.save()

    # Supprimez les données de la session après validation
    if 'reservation_data' in request.session:
        del request.session['reservation_data']

    return render(request, 'reservation/validation.html', {
        'message': 'Réservation confirmée !',
        'box': box,
        'date': date,
        'start_time': start_time,
        'end_time': end_time,
    })


def home(request):
    if request.method == 'POST':
        form = BoxReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirection après la réservation
    else:
        form = BoxReservationForm()
    return render(request, 'home.html', {'form': form})







