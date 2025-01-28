

from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('index_admin/', views.admin_dashboard, name='index_admin'),
    path('modifier_reservationAdmin/<int:reservation_id>/', views.modifier_reservation, name='modifier_reservationAdmin'),
    path('confirmation_annulationAdmin/<int:id>/', views.annuler_reservationAdmin, name='annuler_reservationAdmin'),
    path('administration/', views.admin_dashboard, name='admin_dashboard'),
    path('administration/historique/', views.historique_reservations, name='historique_reservations'),
    path('administration/admin/reservations/', views.admin_reservations, name='index_admin'),
    path('reservation_admin/reservations/', views.reservation_admin, name='reservation_admin'),
]