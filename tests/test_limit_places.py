import pytest
from flask import Flask
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_purchase_more_than_12_places(client):
    # Simuler un club et une compétition
    club_name = 'Simply Lift'
    competition_name = 'Spring Festival'

    # Effectuer une tentative de réservation de 13 places (plus de 12)
    response = client.post('/purchasePlaces', data={
        'competition': competition_name,
        'club': club_name,
        'places': '13'
    })

    # Vérifier que le message d'erreur est affiché
    assert b"You cannot book more than 12 places for a competition." in response.data

def test_purchase_less_than_or_equal_to_12_places(client):
    # Simuler un club et une compétition
    club_name = 'Simply Lift'
    competition_name = 'Spring Festival'

    # Effectuer une tentative de réservation de 10 places (moins de 12)
    response = client.post('/purchasePlaces', data={
        'competition': competition_name,
        'club': club_name,
        'places': '10'
    })

    # Vérifier que la réservation a été effectuée avec succès
    assert b'Great-booking complete! Points have been deducted.' in response.data
