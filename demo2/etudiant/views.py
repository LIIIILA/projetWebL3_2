from django.shortcuts import render, get_object_or_404
from .models import Salle
from .forms import ReservationForm

def index(request):
    return render(request, 'etudiant/index.html')

def login_etudiant(request):
    return render (request,'etudiant/login_etudiant.html')

def historique(request):
    return render(request, 'historique.html')

# def disponibilites(request):
#     salles = Salle.objects.prefetch_related('boxes')
#     return render(request, 'etudiant/disponibilites.html', {'disponibilites': disponibilites})

# def disponibilites_view(request):
#     salles = Salle.objects.all()
#     disponibilites = Disponibilite.objects.all()

#     # Application des filtres si présents dans la requête
#     if 'salle' in request.GET:
#         salles = salles.filter(id=request.GET['salle'])
#     if 'date' in request.GET:
#         disponibilites = disponibilites.filter(jour=request.GET['date'])

#     context = {
#         'salles': salles,
#         'disponibilites': disponibilites
#     }
#     return render(request, 'disponibilites.html', context)
def disponibilites(request):
    salles = Salle.objects.all()
    context = {
        'salles': salles,
    }
    return render(request, 'etudiant/disponibilites.html', context)

def reserver_box(request):
    # Logique pour gérer les réservations
    if request.method == "POST":
        # Traitement du formulaire
        pass
    return render(request, 'etudiant/reserver_box.html')