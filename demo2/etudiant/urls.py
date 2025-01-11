from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),# Page d'accueil de l'application étudiant

    path('login_etudiant/', views.login_etudiant, name='login_etudiant'),
    path('historique/', views.historique, name='historique'),
    path('disponibilites/', views.disponibilites, name='disponibilites'),
    path('reserver/', views.reserver_box, name='reserver_box'),

    path('login/', views.login_view, name='login'),
    path('verify_code/', views.verify_code, name='verify_code'),

]
