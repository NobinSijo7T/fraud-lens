import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health():
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_datasets_are_discovered():
    response = client.get('/api/v1/datasets')
    assert response.status_code == 200
    assert any(item['id'] == 'creditcard/creditcard.csv' for item in response.json()['items'])
    assert any(item['id'] == 'paysim/PS_20174392719_1491204439457_log.csv' for item in response.json()['items'])

def test_invalid_dataset_is_rejected():
    response = client.post('/api/v1/datasets/select', json={'dataset_id':'..\\secret.csv'})
    assert response.status_code == 404

def test_prediction_requires_schema():
    response = client.post('/api/v1/predict/transaction', json={'data':{}})
    assert response.status_code == 422
