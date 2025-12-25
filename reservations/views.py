from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from .models import Logement, Reservation
from .serializers import LogementSerializer, ReservationSerializer
from .forms import LogementForm, ReservationForm


class HomeView(TemplateView):
    """Vue pour la page d'accueil du site."""
    template_name = 'reservations/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logements_count'] = Logement.objects.count()
        context['reservations_count'] = Reservation.objects.count()
        return context


class CreateLogementView(CreateView):
    """Vue pour créer un nouveau logement."""
    model = Logement
    form_class = LogementForm
    template_name = 'reservations/logement_form.html'
    success_url = reverse_lazy('reservations:logement-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        #messages.success(self.request, 'Le logement a été créé avec succès !')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nouveau logement'
        return context


class LogementListCreateView(generics.ListCreateAPIView):
    """
    Vue pour lister et créer des logements.
    
    GET /api/logements/ : Liste tous les logements (JSON)
    GET /logements/ : Page HTML listant les logements
    POST /api/logements/ : Crée un nouveau logement (JSON)
    """
    queryset = Logement.objects.all()
    serializer_class = LogementSerializer
    template_name = 'reservations/logement_list.html'
    
    def get(self, request, *args, **kwargs):
        # Si c'est une requête API, utilisez le comportement par défaut
        if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            return self.list(request, *args, **kwargs)
        
        # Affiche le template HTML avec tous les logements et le formulaire
        logements = self.get_queryset()
        form = LogementForm()
        return render(request, self.template_name, {
            'logements': logements,
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        # Si c'est une requête API, utilisez le comportement par défaut
        if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            return self.create(request, *args, **kwargs)
            
        # Traitement du formulaire HTML
        form = LogementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            #messages.success(request, 'Le logement a été ajouté avec succès !')
            return redirect('logement-list')
            
        # Si le formulaire n'est pas valide, on réaffiche la liste avec les erreurs
        logements = self.get_queryset()
        return render(request, self.template_name, {
            'logements': logements,
            'form': form
        })


class CreateReservationView(FormView):
    """Vue pour créer une nouvelle réservation."""
    template_name = 'reservations/reservation_form.html'
    form_class = ReservationForm
    success_url = reverse_lazy('reservations:reservation-list')
    
    def get_initial(self):
        """Initialise le formulaire avec le logement sélectionné si fourni dans l'URL."""
        initial = super().get_initial()
        logement_id = self.kwargs.get('logement_id')
        if logement_id:
            initial['logement'] = logement_id
        return initial
    
    def form_valid(self, form):
        """Traitement du formulaire valide."""
        form.save()
        #messages.success(self.request, 'La réservation a été créée avec succès !')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """Ajoute des données supplémentaires au contexte du template."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nouvelle réservation'
        return context


class ReservationListCreateView(generics.ListCreateAPIView):
    """
    Vue pour lister et créer des réservations.
    
    GET /api/reservations/ : Liste toutes les réservations (JSON)
    GET /reservations/ : Page HTML listant les réservations
    POST /api/reservations/ : Crée une nouvelle réservation (JSON)
    """
    queryset = Reservation.objects.all().select_related('logement')
    serializer_class = ReservationSerializer
    template_name = 'reservations/reservation_list.html'
    
    def get(self, request, *args, **kwargs):
        # Si c'est une requête API, utilisez le comportement par défaut
        if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            return self.list(request, *args, **kwargs)
        
        # Affiche le template HTML avec toutes les réservations et le formulaire
        reservations = self.get_queryset()
        form = ReservationForm()
        return render(request, self.template_name, {
            'reservations': reservations,
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        # Si c'est une requête API, utilisez le comportement par défaut
        if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            return self.create(request, *args, **kwargs)
            
        # Traitement du formulaire HTML
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            #messages.success(request, 'La réservation a été enregistrée avec succès !')
            return redirect('reservation-list')
            
        # Si le formulaire n'est pas valide, on réaffiche la liste avec les erreurs
        reservations = self.get_queryset()
        return render(request, self.template_name, {
            'reservations': reservations,
            'form': form
        })
    
    def create(self, request, *args, **kwargs):
        """
        Crée une nouvelle réservation.
        
        Args:
            request: Requête HTTP contenant les données de la réservation
            
        Returns:
            Response: Réponse HTTP avec les données de la réservation créée
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        
        # Redirige vers la liste des réservations après création depuis le formulaire HTML
        return render(
            request,
            self.template_name,
            {
                'reservations': self.get_queryset(),
                'success_message': 'Réservation créée avec succès!'
            },
            status=status.HTTP_201_CREATED
        )
