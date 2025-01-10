
from django.shortcuts import redirect, render, get_object_or_404
from .models import Box, Reservation, Site
#from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.db.models import Q

# Create your views here.
from datetime import datetime, timedelta
from datetime import datetime, timedelta

def reservation_index(request):
    hours = [] 
    start_time = datetime.strptime("08:30", "%H:%M")
    end_time = datetime.strptime("18:45", "%H:%M")
    
    current_time = start_time
    while current_time <= end_time:
        hours.append(current_time.strftime('%H:%M'))  # Ajouter l'heure formatée à la liste
        current_time += timedelta(minutes=15)         # Ajouter 15 minutes

    #######################################################################
        
    sites = Site.objects.all()  # Récupère tous les sites de réservation

    if request.method == 'POST':
        site_id = request.POST.get('site_id')  # ID du site sélectionné
        date = request.POST.get('date')  # Récupérer la date choisie
        start_time = request.POST.get('start_time')  # Heure de début
        end_time = request.POST.get('end_time')  # Heure de fin

        try:
            # Combiner la date et les heures en objets datetime
            start_datetime = datetime.strptime(f"{date} {start_time}", "%d-%m-%Y %H:%M")
            end_datetime = datetime.strptime(f"{date} {end_time}", "%d-%m-%Y %H:%M")
        except ValueError:
            return render(request, 'reservation/index.html', {
                'sites': sites,
                'hours': hours,
                'error': 'Format de date ou d\'heure invalide.',
            })


        # Rediriger vers la page des boxes disponibles avec les paramètres
        return redirect('disponibilite_boxes', site_id=site_id, start_time=start_time, end_time=end_time,date=date)
    
    return render(request, 'reservation/index.html', {'sites': sites,'hours': hours})


def disponibilite_boxes(request, site_id, start_time, end_time, date):
    try:
        # Convertir les chaînes en objets datetime
        start_time = datetime.strptime(f"{date} {start_time}", "%d-%m-%Y %H:%M")
        end_time = datetime.strptime(f"{date} {end_time}", "%d-%m-%Y %H:%M")
    except ValueError as e:
        return render(request, 'reservation/disponibilite_boxes.html', {
            'error': f"Format de date ou d'heure invalide : {e}"
        })
    
    # Filtrer les boxes ouvertes dans la plage horaire demandée
    all_boxes = Box.objects.filter(
        site_id=site_id,
        opening_time__lte=start_time.time(),  # Comparer avec l'heure d'ouverture
        closing_time__gte=end_time.time()     # Comparer avec l'heure de fermeture
    )

    print("All boxes:", all_boxes)  # Log pour voir si des boxes sont récupérées

    # Filtrer les réservations qui chevauchent la plage horaire
    overlapping_reservations = Reservation.objects.filter(
        box__site_id=site_id,
        date=start_time.date(),  # Filtrer par la date
        start_time__lt=end_time.time(),  # Réservations qui commencent avant l'heure de fin
        end_time__gt=start_time.time()   # Réservations qui se terminent après l'heure de début
    ).values_list('box_id', flat=True)

    print("Overlapping reservations:", overlapping_reservations)  # Log pour vérifier les réservations qui chevauchent

    # Exclure les boxes réservées
    available_boxes = all_boxes.exclude(id__in=overlapping_reservations)

    print("Available boxes:", available_boxes)  # Log pour voir les boxes disponibles

    return render(request, 'reservation/disponibilite_boxes.html', {
        'boxes': available_boxes,
        'start_time': start_time,
        'end_time': end_time,
        'site_id': site_id,
    })

def index_page_reservation(request):
    reservations = Reservation.objects.all()
    boxes = Box.objects.all()  # Récupérer toutes les boxes
    return render(request, 'reservation/index_page_reservation.html', {'boxes': boxes,'reservations': reservations}) 











''' gestion reservation 15min
def get_available_slots(box, date):
    opening = datetime.combine(date, box.opening_time)
    closing = datetime.combine(date, box.closing_time)
    delta = timedelta(minutes=15)
    slots = []

    # Générer les tranches horaires
    current = opening
    while current + delta <= closing:
        slots.append(current)
        current += delta

    # Exclure les créneaux déjà réservés
    reservations = Reservation.objects.filter(box=box, start_time__date=date)
    for reservation in reservations:
        reserved_start = reservation.start_time
        reserved_end = reservation.end_time
        slots = [slot for slot in slots if not (reserved_start <= slot < reserved_end)]

    return slots


def reserve_box(request, box_id):
    #box = Box.objects.get(id=box_id)
    box = get_object_or_404(Box, id=box_id)
    date = datetime.today().date()
    available_slots = get_available_slots(box, date)

    if request.method == "POST":
        slot = request.POST.get('slot')  # Format : "YYYY-MM-DD HH:MM"
        slot_datetime = datetime.fromisoformat(slot)
        if slot_datetime.date() < datetime.today().date() or slot_datetime.weekday() >= 5:
            return JsonResponse({'error': "Les réservations ne sont pas possibles à cette date."}, status=400)

        Reservation.objects.create(
            box=box,
            student=request.user,
            start_time=slot_datetime,
            end_time=slot_datetime + timedelta(minutes=15)
        )
        return render(request, 'reservation/reserve_box.html', {'box': box})

    return render(request, 'reserve_box.html', {
        'box': box,
        'available_slots': available_slots
    })

'''





'''
@login_required
def reservation_list(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'Reservation/reservation_list.html', {'reservations': reservations})

@login_required
def make_reservation(request, box_id):
    box = get_object_or_404(Box, id=box_id)
    if request.method == 'POST':
        # Traitement de la réservation ici
        pass
    return render(request, 'Reservation/make_reservation.html', {'box': box})
'''