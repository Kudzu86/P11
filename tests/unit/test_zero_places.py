import pytest
from server import app

def test_zero_places():
    with app.test_client() as client:
        app.config['TESTING'] = True
        app.config['CLUBS'] = [{'name': 'Simply Lift', 'points': '20'}]
        app.config['COMPETITIONS'] = [{'name': 'Spring Festival', 'date': '2024-03-27 10:00:00', 'numberOfPlaces': '20'}]
        response = client.post('/purchasePlaces', data={
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '0'
        })
        assert b"You cannot book a negative or zero number of places." in response.data