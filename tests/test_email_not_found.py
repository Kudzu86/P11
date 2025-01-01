import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_email_not_found(client):
    # Essayer de se connecter avec un email inexistant
    response = client.post('/showSummary', data={'email': 'nonexistent@email.com'}, follow_redirects=True)
    # Vérifier que la page d'accueil est rendue après la redirection
    assert b"Welcome to the GUDLFT Registration Portal" in response.data
    assert b"Please enter your secretary email to continue:" in response.data
