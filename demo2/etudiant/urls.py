from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),# Page d'accueil de l'application étudiant
    path('login/', views.login_view, name='login'),
    path('verify_code/', views.verify_code, name='verify_code'),
]
