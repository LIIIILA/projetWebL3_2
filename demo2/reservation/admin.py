from django.contrib import admin
from .models import Box, Reservation,Site,plageHoraire

# Register your models here.

admin.site.register(Box)
admin.site.register(Site)


# class ReservationAdmin(admin.ModelAdmin):
#     list_display = ('id_etudiant','boxe','site', 'start_time', 'end_time')
#     search_fields = ('site',)

# admin.site.register(Reservation, ReservationAdmin)

class ReservationAdmin(admin.ModelAdmin):
    # Liste des champs à afficher dans la liste d'admin
    list_display = ('etudiant_nom', 'box_nom', 'date')  # 'box_nom' et 'etudiant_nom' doivent être des méthodes valides
    list_filter = ('box', 'date')

    # Méthode pour afficher le nom de l'étudiant
    def etudiant_nom(self, obj):
        return obj.id_etudiant.nom  # Assurez-vous que 'id_etudiant' est un champ valide de Reservation

    # Méthode pour afficher le nom de la box (salle)
    def box_nom(self, obj):
        return obj.box.nom  # 'box' doit être une relation valide dans Reservation

    # Définir un nom plus lisible dans l'interface d'administration
    etudiant_nom.short_description = 'Étudiant'
    box_nom.short_description = 'Salle'

# Enregistrement du modèle Reservation avec la classe ReservationAdmin
admin.site.register(Reservation, ReservationAdmin)

class PlageHoraireAdmin(admin.ModelAdmin):
    list_display = ('site', 'start_time', 'end_time')
    search_fields = ('site',)

admin.site.register(plageHoraire, PlageHoraireAdmin)