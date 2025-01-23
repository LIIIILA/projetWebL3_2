from django.shortcuts import render
from .models import Timeslot


# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Reservation, User


def administration_index(request):
    reservations = Reservation.objects.all()
    return render(request, 'administration_index.html', {'reservations': reservations})

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:  # Vérifie si l'utilisateur est un admin
        return redirect('home')  # Redirige si l'utilisateur n'a pas les droits
    reservations = Reservation.objects.all()
    rooms = Room.objects.all()
    users = User.objects.all()
    return render(request, 'admin_dashboard.html', {
        'reservations': reservations,
        'rooms': rooms,
        'users': users
    })

@login_required
def manage_rooms(request):
    if not request.user.is_staff:
        return redirect('home')
    rooms = Room.objects.all()
    return render(request, 'manage_rooms.html', {'rooms': rooms})

@login_required
def manage_users(request):
    if not request.user.is_staff:
        return redirect('home')
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

@login_required
def manage_reservations(request):
    if not request.user.is_staff:
        return redirect('home')
    reservations = Reservation.objects.all()
    return render(request, 'manage_reservations.html', {'reservations': reservations})