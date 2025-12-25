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

