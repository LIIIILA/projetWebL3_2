from django import forms
from reservation.models import Reservation
from etudiant.models import Etudiant

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['id_etudiant', 'box', 'start_time', 'end_time', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'heure_debut': forms.TimeInput(attrs={'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        from etudiant.models import Etudiant  # Import ici pour éviter une dépendance circulaire
        super().__init__(*args, **kwargs)
