# Cocoonr Booking

Application de gestion de réservations de logements.

## Modèles de Données (fichier reservations/models.py)

### Logement
Le modèle `Logement` représente un logement disponible à la location avec les champs suivants :
- `nom` : Nom unique du logement (CharField, max 255 caractères)
- `capacite` : Nombre maximum de personnes que peut accueillir le logement (PositiveIntegerField)

### Réservation
Le modèle `Reservation` représente une réservation de logement avec les champs suivants :
- `logement` : Clé étrangère vers le modèle Logement (relation plusieurs-à-un)
- `date_arrivee` : Date d'arrivée du séjour (DateField)
- `date_depart` : Date de départ (DateField)
- `nom_client` : Nom du client (CharField, max 255 caractères)
- `nb_voyageurs` : Nombre de personnes (PositiveIntegerField)

## Prévention des Chevauchements de Réservations

La méthode `est_periode_disponible` permet de vérifier si un logement est disponible pour une période donnée en évitant les chevauchements de réservations. Voici comment elle fonctionne :

1. **Vérification des dates** : Elle s'assure que la date de départ est postérieure à la date d'arrivée.

2. **Recherche de chevauchements** : Elle recherche toutes les réservations existantes pour le logement qui pourraient chevaucher la période demandée en utilisant la condition :
   ```python
   date_arrivee__lte=date_depart  # La date d'arrivée est avant ou égale à la date de départ demandée
   date_depart__gte=date_arrivee  # ET la date de départ est après ou égale à la date d'arrivée demandée
   ```

3. **Gestion des mises à jour** : Si un `reservation_id` est fourni (cas d'une mise à jour), elle exclut cette réservation de la recherche pour éviter un conflit avec elle-même.

4. **Retour du résultat** : Retourne `True` si aucune réservation ne chevauche la période, `False` sinon.

## Installation

1. **Cloner le dépôt** :
   ```bash
   git clone [URL_DU_DEPOT]
   cd cocoonr_booking
   ```

2. **Créer un environnement virtuel** (recommandé) :
   ```bash
   python uv venv
   source venv/bin/activate  # Sur Linux/Mac
   # OU
   .\venv\Scripts\activate  # Sur Windows
   ```

3. **Installer les dépendances** :
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Appliquer les migrations** :
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Créer un superutilisateur** (optionnel) :
   ```bash
   python manage.py createsuperuser
   ```

## Lancement du Serveur

1. **Démarrer le serveur de développement** :
   ```bash
   python manage.py runserver
   ```

2. **Accéder à l'application** :
   - Ouvrez votre navigateur web préféré
   - Visitez l'URL suivante : http://127.0.0.1:8000/

