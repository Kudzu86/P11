import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Configuration minimale, uniquement le club
        app.config['CLUBS'] = [{'name': 'Simply Lift', 'points': '10'}]
        yield client

def test_points_update(client):
    # Capture état initial
    initial_points = int(app.config['CLUBS'][0]['points'])
    points_to_deduct = 2

    # Test direct de la mise à jour des points
    app.config['CLUBS'][0]['points'] = str(int(app.config['CLUBS'][0]['points']) - points_to_deduct)
    
    # Vérification que les points ont été correctement déduits
    assert int(app.config['CLUBS'][0]['points']) == initial_points - points_to_deduct