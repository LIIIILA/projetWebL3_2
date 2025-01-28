
from pyexpat.errors import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Box, Reservation, Site
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import Etudiant
from icalendar import Calendar, Event
from django.core.mail import EmailMessage
from io import BytesIO
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils import timezone

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

def get_details_modification(session):
    details_modification = session.get('details_modification')
    if not details_modification:
        return None  

    box_id = details_modification['box_id']
    selected_hour = details_modification['selected_hour']
    date = details_modification['date']
    reservation_id=details_modification['reservation_id']

    box = get_object_or_404(Box, id=box_id) 
    start_time = datetime.strptime(selected_hour, '%H:%M')
    end_time = start_time + timedelta(minutes=15)

    return {
        'box': box,
        'date': date,
        'start_time': start_time,
        'end_time': end_time,
        'reservation_id':reservation_id
    }
def reservation_index(request,reservation_id=None):
    # Générer les horaires possibles
    hours = genration_horaires()
    sites = get_sites()
    
    if request.method == 'POST':
        site_id = request.POST.get('site_id')  # ID du site sélectionné
        date = request.POST.get('date')        # Date choisie
        start_time = request.POST.get('start_time')  # Heure de début
        end_time = request.POST.get('end_time')      # Heure de fin
        reservation_id = request.POST.get('reservation_id')
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
            
            if reservation_id : 
                print("reservation_id : ",reservation_id)
                return redirect('disponibilite_boxes',reservation_id=reservation_id, site_id=site_id, date=date, start_time=start_time, end_time=end_time)

            return redirect('disponibilite_boxes', site_id=site_id, date=date, start_time=start_time, end_time=end_time)

    # Si ce n'est pas une requête POST, afficher le formulaire
    return render(request, 'reservation/index.html', {
        'sites': sites,
        'hours': hours,
    })


def disponibilite_boxes(request, site_id=None, date=None, start_time=None, end_time=None, reservation_id=None):
    today = datetime.now()

    if start_time is None:
        start_time = '08:30'  # Heure de début par défaut
    
    if end_time is None:
        end_time = '18:45'  # Heure de fin par défaut
    
    if site_id is None:
        site_id =  1  
    
    if date is None:
        date = today.strftime("%d-%m-%Y")
    
    hours = genration_horaires()
    sites = get_sites()

    print("PRINTER IDD1",reservation_id)

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

    existing_reservation = None
    if reservation_id:
        print("PRINTER IDD",reservation_id)
        existing_reservation = get_object_or_404(Reservation, id=reservation_id)
    
    reservation_idP=reservation_id
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

    if existing_reservation:
        overlapping_reservations = overlapping_reservations.exclude(id=existing_reservation.id)
    
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
    
    # Si c'est une requête POST, traiter les nouvelles données (modification ou création)
    if request.method == "POST":
        box_id = request.POST.get("box_id")
        selected_hour = request.POST.get("selected_hour")
        reservation_id=request.POST.get("reservation_id")
        new_date = request.POST.get("date")
        try:
            box = get_object_or_404(Box, id=box_id)

            # Enregistrer les détails dans la session
            request.session['details_modification'] = {
                'box_id': box.id,
                'box_name': box.nom,
                'site_name': box.site.nom,
                'selected_hour': selected_hour,
                'date': new_date,
                'reservation_id': reservation_id,  
            }
            print("JTMPAS / ",reservation_id)
            details_modification = request.session.get('details_modification')
            print(details_modification)
            messages.success(request, "Détails enregistrés. Veuillez confirmer votre modification.")
            return redirect('verification')

        except Exception as e:
            messages.error(request, f"Erreur : {str(e)}")

    
    return render(request, 'reservation/disponibilite_boxes.html', {
        'disponibilites': disponibilites,
        'start_time': start_datetime,
        'end_time': end_datetime,
        'site_id': site_id,
        'date':  start_datetime.strftime("%Y-%m-%d"),
        'hours': hours,
        'sites': sites,
        'reservation_id' :reservation_id
    })

def verification(request):
    print(f"Session ID dans verification: {request.session.session_key}")
    print(f"Données de la session dans verification: {dict(request.session.items())}")
    print(f"Utilisateur authentifié ? {request.user.is_authenticated}")

    details_reservation = request.session.get('details_reservation')
    details_modification = request.session.get('details_modification')

    if request.method == 'POST' and not details_reservation:
        details_reservation = None 
        box_id = request.POST.get('box_id')
        selected_hour = request.POST.get('selected_hour')
        date = request.POST.get('date')
        print(f"Date: {date}, Box ID: {box_id}, Selected Hour: {selected_hour}") 
        
        request.session['details_reservation'] = {
                'box_id': box_id,
                'selected_hour': selected_hour,
                'date': date,
        }
        details_reservation = request.session['details_reservation']

    print(f"Détails de la réservation : {details_reservation}")    
    
    deta = request.session.get('details_reservation')
    print(deta)

    print(request.user.is_authenticated)
    print(request.user)
    
    if not request.user.is_authenticated:
        print("L'utilisateur n'est pas connecté.")
        return redirect("/etudiant/login/?next=/etudiant/reservation/verification/")

    if not isinstance(request.user, Etudiant):
        print("L'utilisateur connecté n'est pas un étudiant.")
        return redirect("/etudiant/login/?next=/etudiant/reservation/verification/")

    details_reservation = get_details_reservation(request.session)
    
    if not details_reservation and not details_modification:
        print("donnée manquante de details_reservation",details_reservation)
        return redirect('disponibilite_boxes')  
    
    if details_modification : 
        print("Détails de la modif :", details_modification)
        is_modification = details_modification.get('reservation_id') is not None
        details_modification=get_details_modification(request.session)

        if is_modification:
            return render(request, 'reservation/verification.html', {
                'message': 'Veuillez valider votre modification de réservation.',
                'box':details_modification['box'],
                'date':details_modification['date'],
                'start_time': details_modification['start_time'],
                'end_time': details_modification['end_time'],
                'is_modification' : is_modification
        })
    
    if Reservation.objects.filter(id_etudiant=request.user, date=details_reservation['date']).count() >= 4:
        print("Limite de 3 réservations atteinte pour cette journée.")
        messages.error(request, "Vous avez atteint la limite de 4 réservations pour cette journée.")
        return redirect('profil')  # Redirige vers la page d'accueil ou une autre page de ton choix

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
    details_reservation = request.session.get('details_reservation')
    details_modification = request.session.get('details_modification')
    
    details_reservation = get_details_reservation(request.session)
    details_modification = get_details_modification(request.session)

    if not details_reservation and not details_modification:
        print("DEBUG:")
        print(f"details_reservation: {details_reservation}")
        print(f"details_modification: {details_modification}")
        return redirect('reservation_index')  # Redirige si aucune donnée n'est trouvée
    
    is_modification = details_modification is not None and details_modification.get('reservation_id') is not None
    print("MODIFIER",is_modification)

    if is_modification:
        reservation = get_object_or_404(Reservation, id=details_modification['reservation_id'])
        reservation.box = details_modification['box']
        reservation.date = details_modification['date']
        reservation.start_time = details_modification['start_time']
        reservation.end_time = details_modification['end_time']
        reservation.save()
        messages.success(request, "Réservation modifiée avec succès.")
    else:
        reservation = Reservation(
            box=details_reservation['box'],
            id_etudiant=request.user,
            date=details_reservation['date'],
            start_time=details_reservation['start_time'],
            end_time=details_reservation['end_time']
        )
        reservation.save()
        messages.success(request, "Réservation effectuée avec succès.")
    
    mail_confirmation(reservation)
    print(f"Réservation confirmée : Box ID: {reservation.box}, Hour: {reservation.start_time}-{reservation.end_time}, Date: {reservation.date}")

    # Supprimez les données de la session après validation
    if 'details_reservation' in request.session:
        del request.session['details_reservation']
    if 'details_modification' in request.session:
        del request.session['details_modification']
    return render(request, 'reservation/validation.html', {
        'reservation' : reservation
    })





def mail_confirmation(reservation):
    cal = Calendar()
    event = Event()
    event.add('summary', f"Réservation Salle de travaille - Box {reservation.box.nom}")
    event.add('dtstart', reservation.start_time)
    event.add('dtend', reservation.end_time)
    reservation_date = datetime.strptime(reservation.date, "%Y-%m-%d").date()   
    dtstamp = datetime.combine(reservation_date, reservation.start_time.time())
    event.add('dtstamp', dtstamp)
    event.add('location', f"{reservation.box.site.nom}")
    organizer_email = reservation.id_etudiant.email
    organizer_name = reservation.id_etudiant
    event.add('organizer', f'CN="{organizer_name}":mailto:{organizer_email}')
    event.add('description', f"""
    Réservation confirmée :
    - Box : {reservation.box.nom}
    - Site : {reservation.box.site.nom}
    - Date : {reservation.date}
    - Heure de début : {reservation.start_time.strftime('%H:%M')}
    - Heure de fin : {reservation.end_time.strftime('%H:%M')}
    """)

    cal.add_component(event)

    # Écrit le fichier `.ics` en mémoire
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




@login_required
@login_required
def annuler_reservationUser(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        print(f"DEBUG Réservation récupérée : {reservation}")
        try:
            reservation.annuler(request.user)  # Méthode annuler vérifie les permissions
            print("DEBUG - Annulation réussie")
            messages.success(request, "La réservation a été annulée avec succès.")
            return redirect(request.GET.get('next', 'profil'))
        except PermissionDenied as e:
            print(f"DEBUG - Permission refusée : {e}")
            messages.error(request, f"Permission refusée : {e}")
        except Exception as e:
            print(f"DEBUG - Erreur : {e}")
            messages.error(request, f"Une erreur est survenue : {e}")
        
        # Redirection après soumission du formulaire
        next_url = request.GET.get('next', 'profil')
        print(f"DEBUG - Redirection vers : {next_url}")
        return redirect(next_url)
    
    # Affichage de la page de confirmation
    return render(request, 'reservation/annuler_reservationUser.html', {'reservation': reservation})


@login_required
def modifier_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == "POST":
        nouvelle_date = request.POST.get("date")
        nouvel_start_time = request.POST.get("start_time")
        nouvel_end_time = request.POST.get("end_time")

        try:
            reservation.modifier(
                user=request.user,
                nouvelle_date=datetime.strptime(nouvelle_date, "%Y-%m-%d").date(),
                nouvel_start_time=datetime.strptime(nouvel_start_time, "%H:%M").time(),
                nouvel_end_time=datetime.strptime(nouvel_end_time, "%H:%M").time(),
            )
            messages.success(request, "La réservation a été modifiée avec succès.")
            return redirect(request.GET.get('next', 'profil'))
        
        except (PermissionDenied, ValueError) as e:
            messages.error(request, str(e))

    return render(request, "reservation/modifier_reservation.html", {"reservation": reservation})
