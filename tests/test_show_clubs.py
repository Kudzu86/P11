import pytest
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_show_clubs(client):
    response = client.get('/showClubs')
    assert response.status_code == 200
    assert b'Clubs' in response.data  # Vérifier que le mot 'Clubs' est dans la réponse

