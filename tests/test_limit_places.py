import pytest
from server import app


@pytest.fixture
def client():
   app.config['TESTING'] = True
   with app.test_client() as client:
       # Données minimales pour tester la limite de places
       app.config['CLUBS'] = [{'name': 'Simply Lift', 'points': '25', 'email': 'john@simplylift.co'}]
       app.config['COMPETITIONS'] = [{'name': 'Spring Festival', 'date': '2024-03-27 10:00:00', 'numberOfPlaces': '25'}]
       yield client

def test_limit_places(client):
   # Test dépassement limite de 12 places
   response = client.post('/purchasePlaces', data={
       'competition': 'Spring Festival',
       'club': 'Simply Lift',
       'places': '13'
   })
   assert b"You cannot book more than 12 places for a competition." in response.data
