# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.administration_index, name='administration_index'),# Page d'accueil de l'application étudiant
# ]

from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('login_admin/', views.admin_login, name='admin_login'),
    path('index_admin/', views.admin_dashboard, name='index_admin'),
    path('modifier/<int:reservation_id>/', views.modifier_reservation, name='modifier_reservation'),
    path('annuler/<int:id>/', views.annuler_reservation, name='annuler_reservation'),
    path('administration/', views.admin_dashboard, name='admin_dashboard'),
    path('administration/historique/', views.historique_reservations, name='historique_reservations'),
    path('administration/admin/reservations/', views.admin_reservations, name='index_admin'),
    path('admin/reservations/', views.reservation_admin, name='reservation_admin'),
]
