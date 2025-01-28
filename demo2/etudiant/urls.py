from django.urls import path ,include  
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    #path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('login/', views.login_view, name='login_view'),
    path('profil/',views.profil,name='profil'),
    path('reservation/', include('reservation.urls')),
]
