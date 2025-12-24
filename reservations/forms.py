from django import forms
from .models import Logement, Reservation
from django.core.validators import MinValueValidator

class BaseForm(forms.ModelForm):
    """Classe de base pour tous les formulaires avec des styles communs"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajoute des classes CSS par défaut à tous les champs
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ in ['TextInput', 'EmailInput', 'NumberInput', 'DateInput']:
                field.widget.attrs.update({'class': 'form-input'})
            elif field.widget.__class__.__name__ == 'Select':
                field.widget.attrs.update({'class': 'select-input'})
            elif field.widget.__class__.__name__ == 'Textarea':
                field.widget.attrs.update({'class': 'form-textarea'})

class LogementForm(BaseForm):
    class Meta:
        model = Logement
        fields = ['nom', 'capacite']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation des placeholders
        self.fields['nom'].widget.attrs['placeholder'] = 'Nom du logement'
        self.fields['capacite'].widget.attrs.update({
            'min': 1,
            'placeholder': 'Nombre de personnes',
            'class': 'number-input'
        })

class ReservationForm(BaseForm):
    class Meta:
        model = Reservation
        fields = ['logement', 'date_arrivee', 'date_depart', 'nom_client', 'nb_voyageurs']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation des champs spécifiques
        self.fields['date_arrivee'].widget.input_type = 'date'
        self.fields['date_depart'].widget.input_type = 'date'
        
        # Personnalisation des placeholders
        self.fields['nom_client'].widget.attrs['placeholder'] = 'Nom complet du client'
        self.fields['nb_voyageurs'].widget.attrs.update({
            'min': 1,
            'placeholder': 'Nombre de voyageurs',
            'class': 'number-input'
        })
        
        # On s'assure que seuls les logements actifs sont affichés
        self.fields['logement'].queryset = Logement.objects.all()
    
    def clean(self):
        cleaned_data = super().clean()
        date_arrivee = cleaned_data.get('date_arrivee')
        date_depart = cleaned_data.get('date_depart')
        logement = cleaned_data.get('logement')
        nb_voyageurs = cleaned_data.get('nb_voyageurs')
        
        if date_arrivee and date_depart:
            if date_arrivee >= date_depart:
                raise forms.ValidationError("La date de départ doit être postérieure à la date d'arrivée.")
                
            # Vérification des disponibilités
            if logement and logement.est_occupe(date_arrivee, date_depart):
                raise forms.ValidationError("Ce logement n'est pas disponible pour les dates sélectionnées.")
        
        if nb_voyageurs and logement and nb_voyageurs > logement.capacite:
            raise forms.ValidationError(f"Ce logement ne peut pas accueillir plus de {logement.capacite} personne(s).")
            
        return cleaned_data
