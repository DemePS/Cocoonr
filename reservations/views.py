from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Logement, Reservation
from .forms import LogementForm, ReservationForm


class HomeView(TemplateView):
    """Vue pour la page d'accueil du site."""
    template_name = 'reservations/home.html'


class LogementListView(ListView):
    """Vue pour afficher la liste des logements."""
    model = Logement
    template_name = 'reservations/logement_list.html'
    context_object_name = 'logements'
    



class LogementCreateView(CreateView):
    """Vue pour créer un nouveau logement."""
    model = Logement
    form_class = LogementForm
    template_name = 'reservations/logement_form.html'
    success_url = reverse_lazy('reservations:logement-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Le logement a été créé avec succès !')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nouveau logement'
        return context


class ReservationListView(ListView):
    """Vue pour afficher la liste des réservations."""
    model = Reservation
    template_name = 'reservations/reservation_list.html'
    context_object_name = 'reservations'
    
    def get_queryset(self):
        return Reservation.objects.select_related('logement').all()


class ReservationCreateView(CreateView):
    """Vue pour créer une nouvelle réservation."""
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/reservation_form.html'
    success_url = reverse_lazy('reservations:reservation-list')

    def form_valid(self, form):
        """Traitement du formulaire valide."""
        response = super().form_valid(form)
        messages.success(self.request, 'La réservation a été créée avec succès !')
        return response
    
    def get_context_data(self, **kwargs):
        """Ajoute des données supplémentaires au contexte du template."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nouvelle réservation'
        return context
