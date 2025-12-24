"""
URLs spécifiques à l'API de l'application reservations.
"""
from django.urls import path
from .views import LogementListCreateView, ReservationListCreateView

app_name = 'reservations_api'

urlpatterns = [
    path('logements/', LogementListCreateView.as_view(), name='logement-list-create'),
    path('reservations/', ReservationListCreateView.as_view(), name='reservation-list-create'),
]
