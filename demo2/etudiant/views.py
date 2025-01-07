from django.shortcuts import render


def index(request):
    return render(request, 'etudiant/index.html')

def login_etudiant(request):
    return render (request,'etudiant/login_etudiant.html')

