from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation_index, name='reservation_index'),
    path('reserve/<int:box_id>/', views.reserve_box, name='reserve_box'),
]
