from django import forms
from .models import Site

class SiteSelectionForm(forms.Form):
    site = forms.ModelChoiceField(queryset=Site.objects.all(), required=True)
