# forms.py
from django import forms

class ReservationForm(forms.Form):
    heure = forms.ChoiceField(
        choices=[
            ("08:30", "08:30"),
            ("09:00", "09:00"),
            ("09:30", "09:30"),
            ("10:00", "10:00"),
        ],
        widget=forms.RadioSelect,
        label="Heure"
    )
    duree = forms.ChoiceField(
        choices=[
            ("00:15", "30 minutes"),
            ("01:15", "1 heure"),
            ("01:30", "1h30"),
            ("01:45", "2 heures"),
            ("02:00", "2h30"),
        ],
        widget=forms.RadioSelect,
        label="Durée"
    )
