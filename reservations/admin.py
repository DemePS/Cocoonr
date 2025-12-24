from django.contrib import admin
from .models import Logement, Reservation

@admin.register(Logement)
class LogementAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour le modèle Logement."""
    list_display = ('nom', 'capacite')
    search_fields = ('nom',)
    list_filter = ('capacite',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour le modèle Reservation."""
    list_display = ('nom_client', 'logement', 'date_arrivee', 'date_depart', 'nb_voyageurs')
    list_filter = ('date_arrivee', 'date_depart', 'logement')
    search_fields = ('nom_client', 'logement__nom')
    date_hierarchy = 'date_arrivee'
