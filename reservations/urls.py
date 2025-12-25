from django.urls import path
from .views import (
    HomeView, 
    LogementListView,
    LogementCreateView,
    ReservationListView,
    ReservationCreateView
)

app_name = 'reservations'

urlpatterns = [
    # Page d'accueil
    path('', HomeView.as_view(), name='home'),
    
    # Vues HTML
    path('logements/', LogementListView.as_view(), name='logement-list'),
    path('logements/nouveau/', LogementCreateView.as_view(), name='logement-create'),
    path('reservations/', ReservationListView.as_view(), name='reservation-list'),
    path('reservations/nouvelle/', ReservationCreateView.as_view(), name='reservation-create'),
]
