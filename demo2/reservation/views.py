from django.shortcuts import redirect, render, get_object_or_404
from .models import Box, Reservation, Site
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import Etudiant
from icalendar import Calendar, Event
from django.core.mail import EmailMessage
from io import BytesIO


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

def get_details_reservation(session):
    details_reservation = session.get('details_reservation')
    if not details_reservation:
        return None  

    box_id = details_reservation['box_id']
    selected_hour = details_reservation['selected_hour']
    date = details_reservation['date']

    box = get_object_or_404(Box, id=box_id) 
    start_time = datetime.strptime(selected_hour, '%H:%M')
    end_time = start_time + timedelta(minutes=15)

    return {
        'box': box,
        'date': date,
        'start_time': start_time,
        'end_time': end_time,
    }

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


def disponibilite_boxes(request, site_id=None, date=None, start_time=None, end_time=None):
    site_id = site_id or 1  
    today = datetime.now()
    date = date or today.strftime("%d-%m-%Y")
    start_time = start_time or "08:30"
    end_time = end_time or "18:45"
    
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
                    if reservation[0] == box.id and reservation[1] <= datetime.strptime(hour, "%H:%M").time() < reservation[2]:
                        is_reserved = True
                        break
               
                disponibilites_crenaux.append({'hour': hour, 'is_reserved': is_reserved})
        
        disponibilites.append({'box': box, 'disponibilites_crenaux': disponibilites_crenaux})

    #print(f"Available boxes: {available_boxes}")

    
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
        
        request.session['details_reservation'] = {
                'box_id': box_id,
                'selected_hour': selected_hour,
                'date': date,
            }

        if not request.user.is_authenticated:
            return redirect("/etudiant/login/?next=/etudiant/reservation/verification/")

        try:
            etudiant = Etudiant.objects.get(id_etudiant=request.user.etudiant) 
        except Etudiant.DoesNotExist:
            return redirect(f"/etudiant/login/?next=/etudiant/reservation/verification/")

        details_reservation = get_details_reservation(request.session)
        
        return render(request, 'reservation/verification.html', {
            'message': 'Veuillez valider la réservation.',
            'box':details_reservation['box'],
            'date':details_reservation['date'],
            'start_time': details_reservation['start_time'],
            'end_time': details_reservation['end_time'],
            })
    


@login_required
def validation(request):
    etudiant = get_object_or_404(Etudiant, id_etudiant=request.user.id_etudiant)

    details_reservation = get_details_reservation(request.session)
    if not details_reservation:
        return redirect('reservation_index')  # Redirige si aucune donnée n'est trouvée
    
    reservation = Reservation(
        box=details_reservation['box'],
        id_etudiant=request.user,
        date=details_reservation['date'],
        start_time=details_reservation['start_time'],
        end_time=details_reservation['end_time']
        )

    reservation.save()
    mail_confirmation(reservation)
    print(f"Réservation confirmée : Box ID: {reservation.box}, Hour: {reservation.start_time}-{reservation.end_time}, Date: {reservation.date}")

    # Supprimez les données de la session après validation
    if 'details_reservation' in request.session:
        del request.session['details_reservation']

    return render(request, 'reservation/validation.html', {
        'reservation' : reservation
    })





def mail_confirmation(reservation):
    cal = Calendar()
    event = Event()
    event.add('summary', f"Réservation Box {reservation.box.nom}")
    event.add('dtstart', reservation.start_time)
    event.add('dtend', reservation.end_time)
    event.add('dtstamp', reservation.start_time)
    event.add('location', f"{reservation.box.site.nom}")
    event.add('description', f"""
    Réservation confirmée :
    - Box : {reservation.box.nom}
    - Site : {reservation.box.site.nom}
    - Date : {reservation.date}
    - Heure de début : {reservation.start_time.strftime('%H:%M')}
    - Heure de fin : {reservation.end_time.strftime('%H:%M')}
    """)

    cal.add_component(event)

    # Écrit le fichier .ics en mémoire
    ics_file = BytesIO()
    ics_file.write(cal.to_ical())
    ics_file.seek(0)  # Repositionne le curseur au début du fichier

    # Prépare l'email
    subject = f"Confirmation de votre réservation - Box {reservation.box.nom}"
    message = f"""
    Bonjour {reservation.id_etudiant.email},

    Nous vous confirmons que votre réservation pour la Box {reservation.box.nom} a été validée.
    Détails de la réservation :
    - Box : {reservation.box.nom}
    - Site : {reservation.box.site.nom}
    - Date : {reservation.date}
    - Durée : {reservation.end_time - reservation.start_time} minutes

    Vous trouverez ci-joint un fichier pour ajouter cette réservation directement à votre calendrier.

    Merci de votre confiance !
    Cordialement,
    L'équipe de réservation
    """
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email='hongreve@gmail.com',
        to=[reservation.id_etudiant.email],
    )

    email.attach(f"reservation_{reservation.id}.ics", ics_file.read(), 'text/calendar')
    email.send()

def annuler_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    return redirect('confirmation_annulation')