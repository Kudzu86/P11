import pytest
from server import app

@pytest.fixture
def client_competition_places():
    app.config['TESTING'] = True
    with app.test_client() as client:
        app.config['CLUBS'] = [{'name': 'Simply Lift', 'points': '50'}]
        app.config['COMPETITIONS'] = [{'name': 'Spring Festival', 'date': '2024-03-27 10:00:00', 'numberOfPlaces': '5'}]
        yield client

def test_exceed_available_places(client_competition_places):
    response = client_competition_places.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '6'
    })
    assert b"Not enough places available in the competition." in response.data