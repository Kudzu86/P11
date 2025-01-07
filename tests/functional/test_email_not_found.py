import pytest
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        app.config['CLUBS'] = [{'name': 'Simply Lift', 'email': 'john@simplylift.co'}]
        yield client

def test_email_not_found(client):
    # Test email invalide avec redirection
    response = client.post('/showSummary', data={'email': 'nonexistent@email.com'}, follow_redirects=True)
    
    assert response.status_code == 200  # Page après redirection
    assert b"Welcome to the GUDLFT Registration Portal" in response.data
    assert b"Please enter your secretary email to continue:" in response.data

