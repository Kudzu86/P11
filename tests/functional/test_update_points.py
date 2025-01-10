import pytest
from server import app

@pytest.fixture
def client():
   # Configuration minimale pour les tests de purchase
   app.config['TESTING'] = True
   with app.test_client() as client:
       # Données de test avec points suffisants pour réservation
       app.config['CLUBS'] = [{'name': 'Simply Lift', 'points': '25', 'email': 'john@simplylift.co'}]
       app.config['COMPETITIONS'] = [{'name': 'Spring Festival', 'date': '2024-03-27 10:00:00', 'numberOfPlaces': '25'}]
       yield client

def test_purchase_places(client):
   # Capture des points avant réservation 
   club = next(c for c in app.config['CLUBS'] if c['name'] == 'Simply Lift')
   initial_points = int(club['points'])

   # Simulation réservation de 2 places
   response = client.post('/purchasePlaces', data={
       'competition': 'Spring Festival',
       'club': 'Simply Lift',
       'places': '2'
   })

   # Vérification réservation réussie
   assert response.status_code == 200  
   assert b'Great-booking complete! Points have been deducted.' in response.data

   # Vérification déduction des points
   updated_club = next(c for c in app.config['CLUBS'] if c['name'] == 'Simply Lift')
   assert int(updated_club['points']) == initial_points - 2