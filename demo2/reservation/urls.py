from django.urls import path
from . import views
from django.shortcuts import render


urlpatterns = [
    path('', views.reservation_index, name='reservation_index'),
    path('disponibilite_boxes/<int:site_id>//<str:date>/<str:start_time>/<str:end_time>/', 
        views.disponibilite_boxes, name='disponibilite_boxes'),
    path('verification/', views.verification, name='verification'),
    path('validation/', views.validation, name='validation'),
    path('success/', lambda request: render(request, 'success.html'), name='success'),
    
]