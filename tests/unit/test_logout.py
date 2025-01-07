import pytest
from server import app

def test_logout():
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['email'] = 'test@test.com'
        response = client.get('/logout')
        assert response.status_code == 302
        with client.session_transaction() as sess:
            assert 'email' not in sess