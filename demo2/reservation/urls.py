from django.urls import path
from . import views
urlpatterns = [
    path('', views.reservation_index, name='reservation_index'),
    path('disponibilite_boxes/<int:site_id>/<str:date>/<str:start_time>/<str:end_time>/', 
         views.disponibilite_boxes, name='disponibilite_boxes'),
    
    path('disponibilite_boxes/', 
         views.disponibilite_boxes, name='disponibilite_boxes'),
    
    path('disponibilite_boxes/<int:reservation_id>/<int:site_id>/<str:date>', 
         views.disponibilite_boxes, name='disponibilite_boxes'),

    path('disponibilite_boxes/<int:reservation_id>/<int:site_id>/<str:date>/<str:start_time>/<str:end_time>/', 
         views.disponibilite_boxes, name='disponibilite_boxes'),

    path('verification/', views.verification, name='verification'),
    path('validation/', views.validation, name='validation'),
    path('annuler_reservationUser/<int:reservation_id>/', views.annuler_reservationUser, name='annuler_reservationUser'),
    path('modifier/<int:reservation_id>/', views.modifier_reservation, name='modifier_reservation'),

]
