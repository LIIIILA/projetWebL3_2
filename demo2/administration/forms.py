from django import forms
from .models import Reservation, TimeSlot
from .models import Reservation
from django.contrib.auth import get_user_model


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['user', 'room', 'start_time', 'end_time']

class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['room', 'start_time', 'end_time', 'is_blocked']

class AdminReservationForm(forms.ModelForm):
    etudiant = forms.ModelChoiceField(queryset=get_user_model().objects.all(), label="Étudiant")  # Sélection d'un étudiant


    class Meta:
        model = Reservation
        fields = ['etudiant', 'box', 'date', 'time_slot']        