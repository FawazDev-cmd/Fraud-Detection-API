from fastapi.testclient import TestClient

from app.api.schemas import FEATURES
from app.main import app

def test_missing_feature_returns_422():
    transaction = {feature: 0.0 for feature in FEATURES}
    transaction.pop("V1")

    with TestClient(app) as client:
        response = client.post("/predict", json=transaction)
    assert response.status_code == 422

def test_extra_field_returns_422():
    transaction = {feature: 0.0 for feature in FEATURES}
    transaction["unexpected_field"] = 1.0

    with TestClient(app) as client:
        response = client.post("/predict", json=transaction)
    assert response.status_code == 422

def test_negative_amount_returns_422():
    transaction = {feature: 0.0 for feature in FEATURES}
    transaction["Amount"] = -1.0

    with TestClient(app) as client:
        response = client.post("/predict", json=transaction)
    assert response.status_code == 422

