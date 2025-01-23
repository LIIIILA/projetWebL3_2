from django.contrib import admin
from .models import Reservation, TimeSlot

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'start_time', 'end_time', 'created_at', 'updated_at')
    list_filter = ('room', 'start_time', 'end_time')
    search_fields = ('user__username', 'room')

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('room', 'start_time', 'end_time', 'is_blocked')
    list_filter = ('room', 'is_blocked')
    search_fields = ('room',)
