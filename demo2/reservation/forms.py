from datetime import datetime
from django import forms
from .models import Site

class SiteSelectionForm(forms.Form):
    site = forms.ModelChoiceField(queryset=Site.objects.all(), required=True)

class ReservationForm(forms.Form):
    site_id = forms.IntegerField()
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    # Méthode de validation pour vérifier la cohérence des dates
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        # Combiner la date et l'heure en datetime pour la validation
        try:
            start_datetime = datetime.combine(date, start_time)
            end_datetime = datetime.combine(date, end_time)

            # Validation de l'ordre des dates
            if start_datetime >= end_datetime:
                raise forms.ValidationError('L\'heure de début doit être avant l\'heure de fin.')
        except Exception as e:
            raise forms.ValidationError(f"Erreur dans la combinaison des dates et heures : {str(e)}")

        return cleaned_data