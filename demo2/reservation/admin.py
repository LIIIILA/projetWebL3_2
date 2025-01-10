from django.contrib import admin
from .models import Box, Reservation,Site,plageHoraire

# Register your models here.

admin.site.register(Box)
admin.site.register(Site)


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id_etudiant','boxe','site', 'start_time', 'end_time')
    search_fields = ('site',)

admin.site.register(Reservation)

class PlageHoraireAdmin(admin.ModelAdmin):
    list_display = ('site', 'start_time', 'end_time')
    search_fields = ('site',)

admin.site.register(plageHoraire, PlageHoraireAdmin)