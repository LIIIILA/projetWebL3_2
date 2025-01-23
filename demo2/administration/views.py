from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Reservation, TimeSlot
from .forms import ReservationForm, TimeSlotForm, AdminReservationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Box, Reservation
from django.contrib.auth.models import User






def administration_index(request):
    reservations = Reservation.objects.all()
    return render(request, 'administration_index.html', {'reservations': reservations})

def create_reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm()
    return render(request, 'admin/create_reservation.html', {'form': form})

@login_required
def update_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'admin/update_reservation.html', {'form': form})

@login_required
def delete_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    if request.method == "POST":
        reservation.delete()
        return redirect('reservation_list')
    return render(request, 'admin/delete_reservation.html', {'reservation': reservation})


@login_required
def create_timeslot(request):
    if request.method == "POST":
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('timeslot_list')
    else:
        form = TimeSlotForm()
    return render(request, 'admin/create_timeslot.html', {'form': form})

@login_required
def update_timeslot(request, timeslot_id):
    timeslot = TimeSlot.objects.get(id=timeslot_id)
    if request.method == "POST":
        form = TimeSlotForm(request.POST, instance=timeslot)
        if form.is_valid():
            form.save()
            return redirect('timeslot_list')
    else:
        form = TimeSlotForm(instance=timeslot)
    return render(request, 'admin/update_timeslot.html', {'form': form})

@login_required
def block_timeslot(request, timeslot_id):
    timeslot = TimeSlot.objects.get(id=timeslot_id)
    timeslot.is_blocked = True
    timeslot.save()
    return redirect('timeslot_list')
#     return render(request, 'manage_reservations.html', {'reservations': reservations})

@login_required
def create_reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm()
    return render(request, 'admin/create_reservation.html', {'form': form})

@login_required
def update_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'admin/update_reservation.html', {'form': form})

@login_required
def delete_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    if request.method == "POST":
        reservation.delete()
        return redirect('reservation_list')
    return render(request, 'admin/delete_reservation.html', {'reservation': reservation})

@login_required
def create_timeslot(request):
    if request.method == "POST":
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('timeslot_list')
    else:
        form = TimeSlotForm()
    return render(request, 'admin/create_timeslot.html', {'form': form})

@login_required
def update_timeslot(request, timeslot_id):
    timeslot = TimeSlot.objects.get(id=timeslot_id)
    if request.method == "POST":
        form = TimeSlotForm(request.POST, instance=timeslot)
        if form.is_valid():
            form.save()
            return redirect('timeslot_list')
    else:
        form = TimeSlotForm(instance=timeslot)
    return render(request, 'admin/update_timeslot.html', {'form': form})

@login_required
def block_timeslot(request, timeslot_id):
    timeslot = TimeSlot.objects.get(id=timeslot_id)
    timeslot.is_blocked = True
    timeslot.save()
    return redirect('timeslot_list')

def admin_dashboard(request):
    return render(request, 'administration/admin_dashboard.html')

def manage_rooms(request):
    # Logique de gestion des salles
    rooms = Box.objects.all()
    return render(request, 'admin/manage_rooms.html', {'rooms': rooms})

def manage_users(request):
    # Logique de gestion des utilisateurs
    users = User.objects.all()
    return render(request, 'admin/manage_users.html', {'users': users})

def create_user(request):
    # Logique pour créer un utilisateur
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserCreationForm()
    return render(request, 'admin/create_user.html', {'form': form})



@login_required
def manage_rooms(request):
    rooms = Box.objects.all()
    return render(request, 'admin/manage_rooms.html', {'rooms': rooms})

def create_reservation_admin(request):
    if not request.user.is_staff:  # Vérifie que l'utilisateur est un administrateur
        return redirect('home')  # Redirige vers la page d'accueil si non autorisé

    if request.method == "POST":
        form = AdminReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservation_list')  # Redirige vers la liste des réservations
    else:
        form = AdminReservationForm()

    return render(request, 'admin/create_reservation_admin.html', {'form': form})

@login_required
def reservation_list(request):
    reservations = Reservation.objects.all()  # Liste de toutes les réservations
    return render(request, 'admin/reservation_list.html', {'reservations': reservations})
