import pytest
import json
from server import app

# Création d'un client de test pour faire les requêtes HTTP
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Fonction pour charger les clubs depuis le fichier clubs.json
def load_clubs():
    with open('clubs.json') as c:
        return json.load(c)['clubs']

# Test de la mise à jour des points lors de la réservation de places
def test_purchase_places(client):
    # Charger les données actuelles des clubs
    clubs = load_clubs()

    # Trouver le club "Simply Lift"
    club = next(c for c in clubs if c['name'] == 'Simply Lift')
    initial_points = int(club['points'])  # Points initiaux
    places_to_book = 2  # Nombre de places à réserver

    # Simuler une requête pour réserver des places
    response = client.post(
        '/purchasePlaces',
        data={'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': str(places_to_book)}
    )

    # Vérifier que la réservation a été effectuée
    assert b'Great-booking complete! Points have been deducted.' in response.data

    # Recharger la liste des clubs après la réservation
    updated_clubs = load_clubs()
    updated_club = next(c for c in updated_clubs if c['name'] == 'Simply Lift')

    # Calculer les points attendus
    expected_points = initial_points - places_to_book

    # Vérifier que le nombre de points du club a bien été mis à jour
    assert int(updated_club['points']) == expected_points
