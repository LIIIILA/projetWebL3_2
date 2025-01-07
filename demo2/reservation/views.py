from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Box, Reservation
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

# Create your views here.

def reservation_index(request):
    reservations = Reservation.objects.all()
    boxes = Box.objects.all()  # Récupérer toutes les boxes
    return render(request, 'reservation/index.html', {'boxes': boxes,'reservations': reservations})



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
