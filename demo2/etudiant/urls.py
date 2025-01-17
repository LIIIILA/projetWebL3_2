from django.urls import path # type: ignore
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),# Page d'accueil de l'application étudiant

    path('connexion/', views.connexion, name='connexion'),
    path('historique/', views.historique, name='historique'),
    path('disponibilites/', views.disponibilites, name='disponibilites'),
    # path('deconnexion/', LogoutView.as_view(), name='logout'),
    path('deconnexion/', views.custom_logout, name='logout'),
    path('reserver/', views.reserver_box, name='reserver_box'),
    path('login/', views.login_view, name='login'),
    path('verify_code/', views.verify_code, name='verify_code'),

]
