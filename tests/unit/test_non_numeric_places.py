import pytest
from server import app

def test_non_numeric_places():
    with app.test_client() as client:
        app.config['TESTING'] = True
        app.config['CLUBS'] = [{'name': 'Simply Lift', 'points': '20'}]
        app.config['COMPETITIONS'] = [{'name': 'Spring Festival', 'date': '2024-03-27 10:00:00', 'numberOfPlaces': '20'}]
        response = client.post('/purchasePlaces', data={
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': 'abc'
        })
        assert b"Invalid input. Please enter a valid number of places." in response.data