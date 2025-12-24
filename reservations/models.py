from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q


class Logement(models.Model):
    """Modèle représentant un logement disponible à la location."""
    nom = models.CharField(max_length=255, verbose_name="Nom du logement")
    capacite = models.PositiveIntegerField(verbose_name="Capacité (nombre de personnes)")

    def __str__(self):
        return f"{self.nom} (jusqu'à {self.capacite} personnes)"

    def est_occupe(self, date_arrivee, date_depart):
        """
        Vérifie si le logement est déjà réservé pour les dates données.
        Retourne True si le logement est occupé, False sinon.
        """
        return self.reservations.filter(
            Q(date_arrivee__lt=date_depart) & 
            Q(date_depart__gt=date_arrivee)
            ).exists()




class Reservation(models.Model):
    """Modèle représentant une réservation de logement."""
    logement = models.ForeignKey(
        Logement,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name="Logement réservé"
    )
    date_arrivee = models.DateField(verbose_name="Date d'arrivée")
    date_depart = models.DateField(verbose_name="Date de départ")
    nom_client = models.CharField(max_length=255, verbose_name="Nom du client")
    nb_voyageurs = models.PositiveIntegerField(verbose_name="Nombre de voyageurs")
    
    class Meta:
        ordering = ['date_arrivee']
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
    
    def __str__(self):
        return f"Réservation de {self.nom_client} du {self.date_arrivee} au {self.date_depart}"

    def chevauchements(self, date_arrivee, date_depart):
        """
        Retourne les réservations qui chevauchent la période donnée.
        """
        reservations = Reservation.objects.filter(
            logement=self.logement
        ).exclude(pk=self.pk).filter(
            Q(date_arrivee__lte=self.date_depart, date_depart__gte=self.date_arrivee)
        )       
        return reservations

    def est_disponible(self, date_arrivee, date_depart):
        """
        Vérifie si le logement est disponible pour les dates données.
        Retourne True si le logement est disponible, False sinon.
        """
        chevauchements = self.chevauchements(date_arrivee, date_depart)

        if chevauchements.exists():
            return False
        else:
            return True
        
        
    
    def clean(self):
        """Valide les données de la réservation avant l'enregistrement."""
        super().clean()
        
        # Vérification des dates
        if self.date_depart <= self.date_arrivee:
            raise ValidationError("La date de départ doit être postérieure à la date d'arrivée.")
        
        # Vérification de la capacité
        if self.nb_voyageurs > self.logement.capacite:
            raise ValidationError(
                f"Le nombre de voyageurs ({self.nb_voyageurs}) dépasse "
                f"la capacité du logement ({self.logement.capacite} personnes)."
            )
        
        # Affiche des périodes de réservation existantes
        chevauchements = self.chevauchements(self.date_arrivee, self.date_depart)
        
        chevauchements_dates = chevauchements.values_list('date_arrivee', 'date_depart')
        
        if chevauchements_dates.exists():
            periodes = [
                f"- Du {arrivee} au {depart}" 
                for arrivee, depart in chevauchements_dates
            ]
            raise ValidationError(
                "Ce logement est déjà réservé pour la période demandée. "
                f"Périodes de réservation existantes :\n" + "\n".join(periodes)
            )
    
    def save(self, *args, **kwargs):
        """Sauvegarde la réservation après validation."""
        self.full_clean()
        super().save(*args, **kwargs)
    
    @classmethod
    def est_periode_disponible(cls, logement, date_arrivee, date_depart, reservation_id=None):
        """
        Vérifie si un logement est disponible pour une période donnée.
        
        Args:
            logement: Instance de Logement
            date_arrivee: Date d'arrivée
            date_depart: Date de départ
            reservation_id: ID de la réservation en cours de modification (optionnel)
            
        Returns:
            bool: True si la période est disponible, False sinon
        """
        if date_depart <= date_arrivee:
            return False
            
        queryset = cls.objects.filter(
            logement=logement,
            date_arrivee__lte=date_depart,
            date_depart__gte=date_arrivee
        )
        
        if reservation_id is not None:
            queryset = queryset.exclude(pk=reservation_id)
            
        return not queryset.exists()
