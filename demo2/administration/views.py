from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Reservation, TimeSlot
from .forms import ReservationForm, TimeSlotForm, AdminReservationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Box, Reservation
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models




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
    return render(request, 'admin/dashboard.html', {'user': request.user})

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


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'adresse email doit être fournie')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser doit avoir is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email



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


def create_superuser(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    if extra_fields.get('is_staff') is not True:
        raise ValueError('Superuser doit avoir is_staff=True.')
    if extra_fields.get('is_superuser') is not True:
        raise ValueError('Superuser doit avoir is_superuser=True.')

    return self.create_user(email, password, **extra_fields)

class AdminLoginView(LoginView):
    template_name = 'administration/login.html'  # Fichier HTML de la page de connexion
    success_url = reverse_lazy('admin_dashboard')  # Page de redirection après connexion

    def get_success_url(self):
        return self.success_url
    
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # Vérifie que l'utilisateur est un administrateur
            login(request, user)
            return redirect('admin_dashboard')  # Remplace 'admin_dashboard' par ta vue
        else:
            messages.error(request, 'Identifiants invalides ou droits insuffisants.')
    return render(request, 'admin/login_admin.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')  # Redirige vers la page de connexion

def is_admin(user):
    return user.is_authenticated and user.is_staff
