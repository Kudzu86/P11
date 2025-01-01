import pytest
from datetime import datetime
from server import app

# Création d'un client de test pour faire les requêtes HTTP
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test de la réservation d'une compétition passée
def test_book_past_competition(client):
    # Simuler une compétition passée avec une date dans le passé
    past_competition = {
        'name': 'Spring Festival',
        'date': '2020-03-27 10:00:00',  # Date passée
        'numberOfPlaces': '25'
    }

    # Simuler un club
    club = {'name': 'Simply Lift'}

    # Simuler la requête pour réserver la compétition passée
    response = client.get(f'/book/{past_competition["name"]}/{club["name"]}')

    # Vérifier que le message d'erreur est affiché
    assert b"Cannot book places for a past competition." in response.data
