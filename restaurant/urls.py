from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('reservations/', views.reservations, name='reservations'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('messageenvoye/', views.recrute, name='messageenvoye'),
    path('reservation_success/', views.reservation_success, name='reservation_success'),
]
