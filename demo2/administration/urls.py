from django.urls import path
from . import views

urlpatterns = [
    path('', views.administration_index, name='administration_index'),# Page d'accueil de l'application étudiant
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-rooms/', views.manage_rooms, name='manage_rooms'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('manage-reservations/', views.manage_reservations, name='manage_reservations'),
]
