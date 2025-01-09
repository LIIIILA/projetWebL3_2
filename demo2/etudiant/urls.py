from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),# Page d'accueil de l'application étudiant
    path('login_etudiant/', views.login_etudiant, name='login_etudiant'),
]
