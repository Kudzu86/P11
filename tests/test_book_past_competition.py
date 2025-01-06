import pytest
from server import app


@pytest.fixture
def client():
   app.config['TESTING'] = True
   with app.test_client() as client:
       # Configuration minimale avec date passée pour tester la validation
       app.config['CLUBS'] = [{'name': 'Simply Lift', 'points': '25'}]
       app.config['COMPETITIONS'] = [{'name': 'Fall Classic', 'date': '2020-10-22 13:30:00', 'numberOfPlaces': '20'}]
       yield client

def test_book_past_competition(client):
   # Vérifie le rejet des réservations pour compétitions passées
   response = client.get('/book/Fall Classic/Simply Lift')
   assert b"Cannot book places for a past competition." in response.data