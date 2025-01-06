import pytest
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        app.config['CLUBS'] = [{'name': 'Simply Lift', 'points': '3', 'email': 'john@simplylift.co'}]
        app.config['COMPETITIONS'] = [{'name': 'Spring Festival', 'date': '2024-03-27 10:00:00', 'numberOfPlaces': '25'}]
        yield client

def test_prevent_negative_points(client):
    # Le club "Simply Lift" a seulement 3 points
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '5'  # Demande de 5 places alors que le club a 3 points
    }, follow_redirects=True)

    # Vérifie que le message flash attendu est bien présent
    assert b"You do not have enough points to book these places." in response.data
