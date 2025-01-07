import pytest
from server import app

@pytest.fixture
def client_places():
    app.config['TESTING'] = True
    with app.test_client() as client:
        app.config['CLUBS'] = [{'name': 'Simply Lift', 'points': '10'}]
        app.config['COMPETITIONS'] = [{'name': 'Spring Festival', 'date': '2024-03-27 10:00:00', 'numberOfPlaces': '20'}]
        yield client

def test_negative_places(client_places):
    response = client_places.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '-1'
    })
    assert b"You cannot book a negative or zero number of places." in response.data