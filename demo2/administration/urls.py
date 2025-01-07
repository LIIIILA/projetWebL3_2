from django.urls import path
from . import views

urlpatterns = [
    path('', views.administration_index, name='administration_index'),# Page d'accueil de l'application étudiant
]
