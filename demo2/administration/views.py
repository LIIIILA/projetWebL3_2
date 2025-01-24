from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from reservation.models import Reservation

def administration_index(request):
    reservations = Reservation.objects.all()
    return render(request, 'administration/administration_index.html', {'reservations': reservations})
from django.shortcuts import render, get_object_or_404, redirect
from .models import Salle, Reservation
from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    reservations = Reservation.objects.all()
    salles = Salle.objects.all()
    return render(request, 'reservation/admin_dashboard.html', {
        'reservations': reservations,
        'salles': salles,
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

@login_required
def annuler_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    return redirect('admin_dashboard')

@login_required
def historique_reservations(request):
    salles = Salle.objects.all()
    historique = None
    salle_selectionnee = None
    if request.method == "POST":
        salle_id = request.POST['salle_id']
        salle_selectionnee = get_object_or_404(Salle, id=salle_id)
        historique = Reservation.objects.filter(salle=salle_selectionnee).order_by('date', 'heure_debut')
    return render(request, 'reservation/admin_dashboard.html', {
        'salles': salles,
        'historique': historique,
        'salle_selectionnee': salle_selectionnee,
    })
