from fastapi.testclient import TestClient

from app.api.schemas import FEATURES
from app.main import app
from unittest.mock import Mock, patch

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

def test_prediction_failure_returns_500():
    transaction = {feature: 0.0 for feature in FEATURES}
    with patch("app.api.routes.predict_transaction", side_effect=RuntimeError("Internal model error")):
        with TestClient(app, raise_server_exceptions= False) as client:
            response = client.post("/predict", json=transaction)
            assert response.status_code == 500
            assert "Internal model error" not in response.text