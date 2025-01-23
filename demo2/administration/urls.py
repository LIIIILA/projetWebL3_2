from django.urls import path
from . import views

urlpatterns = [
    path('', views.administration_index, name='administration_index'),  # Page d'accueil
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Pages de gestion des réservations
    path('create/', views.create_reservation, name='create_reservation'),
    path('reservations/<int:reservation_id>/update/', views.update_reservation, name='update_reservation'),
    path('reservations/<int:reservation_id>/delete/', views.delete_reservation, name='delete_reservation'),
    
    # Pages de gestion des plages horaires
    path('timeslots/create/', views.create_timeslot, name='create_timeslot'),
    path('timeslots/<int:timeslot_id>/update/', views.update_timeslot, name='update_timeslot'),
    path('timeslots/<int:timeslot_id>/block/', views.block_timeslot, name='block_timeslot'),
    
    # Pages de gestion des salles
    path('rooms/', views.manage_rooms, name='manage_rooms'),
    
    # Pages de gestion des utilisateurs (si tu en as besoin)
    path('users/', views.manage_users, name='manage_users'),
    path('create/', views.create_user, name='create_user'),


    path('admin/reservations/create/', views.create_reservation_admin, name='create_reservation_admin'),
]

