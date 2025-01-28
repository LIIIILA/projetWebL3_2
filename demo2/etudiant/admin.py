from django.contrib import admin
from .models import Etudiant

class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('id_etudiant', 'email', 'is_blacklisted',)
    list_filter=('is_blacklisted',)
    ordering=['email']
    search_fields=('id_etudiant',)

admin.site.register(Etudiant, EtudiantAdmin)