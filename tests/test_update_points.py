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
    # Simuler une requête pour réserver 8 places pour un club
    response = client.post('/purchasePlaces', data={'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': '2'})

    # Vérifier que la réservation a été effectuée
    assert b'Great-booking complete! Points have been deducted.' in response.data

    # Charger la liste des clubs après la réservation
    clubs = load_clubs()

    # Vérifier que le nombre de points du club a bien été mis à jour
    club = next(c for c in clubs if c['name'] == 'Simply Lift')
    assert club['points'] == '3'  # Cela vérifiera que la mise à jour est bien effectuée
    

