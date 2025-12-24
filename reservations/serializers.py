from rest_framework import serializers
from .models import Logement, Reservation

class LogementSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Logement."""
    class Meta:
        model = Logement
        fields = ['id', 'nom', 'capacite']

class ReservationSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Reservation avec des champs supplémentaires en lecture seule."""
    logement_nom = serializers.CharField(source='logement.nom', read_only=True)
    logement_capacite = serializers.IntegerField(source='logement.capacite', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'logement', 'logement_nom', 'logement_capacite',
            'date_arrivee', 'date_depart', 'nom_client', 'nb_voyageurs'
        ]
        extra_kwargs = {
            'logement': {'write_only': True}  # Le champ logement n'est pas renvoyé dans la réponse
        }
    
    def validate(self, data):
        """Valide les données de la réservation."""
        logement = data.get('logement')
        date_arrivee = data.get('date_arrivee')
        date_depart = data.get('date_depart')
        nb_voyageurs = data.get('nb_voyageurs')
        
        # Vérification des dates
        if date_depart <= date_arrivee:
            raise serializers.ValidationError(
                "La date de départ doit être postérieure à la date d'arrivée."
            )
            
        # Vérification de la capacité
        if nb_voyageurs > logement.capacite:
            raise serializers.ValidationError(
                f"Le nombre de voyageurs ({nb_voyageurs}) dépasse "
                f"la capacité du logement ({logement.capacite} personnes)."
            )
            
        # Vérification des chevauchements
        queryset = Reservation.objects.filter(
            logement=logement,
            date_arrivee__lt=date_depart,
            date_depart__gt=date_arrivee
        )
        
        # Si c'est une mise à jour, on exclut la réservation actuelle
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
            
        if queryset.exists():
            raise serializers.ValidationError(
                "Ce logement est déjà réservé pour cette période."
            )
            
        return data
