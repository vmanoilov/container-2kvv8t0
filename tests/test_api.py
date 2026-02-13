import pytest
from app.api.main import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.api.main.get_dispatcher')
def test_scan_valid(mock_get_dispatcher, client):
    mock_dispatcher = MagicMock()
    mock_dispatcher.start_scan.return_value = 'test-job-id'
    mock_get_dispatcher.return_value = mock_dispatcher
    response = client.post('/scan', json={'target': 'example.com', 'profile': 'standard'})
    assert response.status_code == 201
    assert response.get_json() == {'job_id': 'test-job-id'}

def test_scan_missing_target(client):
    response = client.post('/scan', json={})
    assert response.status_code == 400

def test_scan_invalid_target(client):
    response = client.post('/scan', json={'target': 'invalid..target'})
    assert response.status_code == 400

def test_scan_invalid_profile(client):
    response = client.post('/scan', json={'target': 'example.com', 'profile': 'invalid'})
    assert response.status_code == 400