from django.contrib import admin
from django.urls import path, include
from etudiant import views

urlpatterns = [
    path('', include('reservation.urls')),  # Page d'accueil redirigée vers l'application "reservation"
    path('admin/', admin.site.urls), 
    path('reservation/', include('reservation.urls')),
    path('etudiant/', include('etudiant.urls')),  # Application 'etudiant' incluse
    path('administration/', include('administration.urls')),

]
