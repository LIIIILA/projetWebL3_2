# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.administration_index, name='administration_index'),# Page d'accueil de l'application étudiant
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('modifier/<int:reservation_id>/', views.modifier_reservation, name='modifier_reservation'),
    path('annuler/<int:reservation_id>/', views.annuler_reservation, name='annuler_reservation'),
    path('historique/', views.historique_reservations, name='historique_reservations'),
]

