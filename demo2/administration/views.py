from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from reservation.models import Reservation

def administration_index(request):
    reservations = Reservation.objects.all()
    return render(request, 'administration/administration_index.html', {'reservations': reservations})
