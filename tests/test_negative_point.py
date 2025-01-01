import pytest

@pytest.fixture
def client():
    from server import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_prevent_negative_points(client):
    # Le club "Simply Lift" a seulement 3 points
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '5'  # Demande de 5 places alors que le club a 3 points
    })
    assert b"You do not have enough points to book these places." in response.data

