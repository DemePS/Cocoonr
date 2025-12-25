from django.urls import path
from .views import (
    HomeView, 
    LogementListCreateView, 
    ReservationListCreateView,
    CreateReservationView,
    CreateLogementView
)

app_name = 'reservations'

urlpatterns = [
    # Page d'accueil
    path('', HomeView.as_view(), name='home'),
    
    # Vues HTML
    path('logements/', LogementListCreateView.as_view(), name='logement-list'),
    path('logements/nouveau/', CreateLogementView.as_view(), name='logement-create'),
    path('reservations/', ReservationListCreateView.as_view(), name='reservation-list'),
    path('reservations/nouvelle/', CreateReservationView.as_view(), name='reservation-create'),
]
