import pytest
from server import app


@pytest.fixture
def client():
   app.config['TESTING'] = True
   with app.test_client() as client:
       # Données de test pour parcours utilisateur complet
       app.config['CLUBS'] = [{'name': 'Simply Lift', 'points': '25', 'email': 'john@simplylift.co'}]
       app.config['COMPETITIONS'] = [{'name': 'Spring Festival', 'date': '2024-03-27 10:00:00', 'numberOfPlaces': '25'}]
       yield client

def test_user_journey(client):
   # Capture état initial
   club = next(c for c in app.config['CLUBS'] if c['name'] == 'Simply Lift')
   competition = next(c for c in app.config['COMPETITIONS'] if c['name'] == 'Spring Festival')
   initial_points = int(club['points'])
   initial_places = int(competition['numberOfPlaces'])

   # Test connexion
   response = client.post('/showSummary', data={'email': club['email']})
   assert response.status_code == 200
   assert f'Welcome, {club["email"]}'.encode() in response.data

   # Test réservation
   places_to_book = 3
   response = client.post('/purchasePlaces', data={
       'competition': competition['name'],
       'club': club['name'],
       'places': str(places_to_book)
   })
   assert response.status_code == 200
   assert b'Great-booking complete! Points have been deducted.' in response.data

   # Vérification mises à jour
   updated_club = next(c for c in app.config['CLUBS'] if c['name'] == club['name'])
   updated_competition = next(c for c in app.config['COMPETITIONS'] if c['name'] == competition['name'])
   assert int(updated_club['points']) == initial_points - places_to_book
   assert int(updated_competition['numberOfPlaces']) == initial_places - places_to_book

   # Test déconnexion
   response = client.get('/logout')
   assert response.status_code == 302
   assert response.location.endswith('/')