# administration/admin.py
from reservation.admin import ReservationAdmin
from reservation.models import Reservation
from django.contrib import admin
<<<<<<< HEAD

=======
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_student', 'is_admin']

admin.site.register(CustomUser, CustomUserAdmin)
>>>>>>> Fin
