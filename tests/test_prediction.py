from fastapi.testclient import TestClient

from app.api.schemas import FEATURES
from app.main import app

def test_predict_transaction():
    transaction = {feature: 0.0 for feature in FEATURES}

    with TestClient(app) as client:
        response = client.post("/predict", json=transaction)
        assert response.status_code == 200
        result = response.json()

        assert "fraud_probability" in result
        assert "is_fraud" in result
        assert "threshold" in result

        assert 0 <= result["fraud_probability"] <= 1
        assert isinstance(result["is_fraud"], bool)
        assert 0 <= result["threshold"] <= 1