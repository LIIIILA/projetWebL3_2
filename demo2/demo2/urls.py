from django.contrib import admin
from django.urls import path, include
from etudiant import views

urlpatterns = [
    path('', include('reservation.urls')),  # Page d'accueil redirigée vers l'application "reservation"
    path('admin/', admin.site.urls), 
    path('reservation/', include('reservation.urls')),
    path('etudiant/', include('etudiant.urls')),  # Application 'etudiant' incluse
    path('administration/', include('administration.urls')),
    
    # Corriger la ligne suivante pour associer directement /login à la vue login_view
    path('login/', views.login_view, name='login'),  # Utilisation directe de la vue de login
    path('send-email/', views.send_test_email, name='send_test_email'),
]
