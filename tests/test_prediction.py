import pytest

from fastapi.testclient import TestClient

from app.api.schemas import FEATURES
from app.main import app
from unittest.mock import Mock, patch

from app.services.prediction_service import predict_transaction

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

def test_invalid_probability_is_rejected():
    transaction = {feature: 0.0 for feature in FEATURES}
    mock_model = Mock()

    mock_model.predict_proba.return_value = [[0.9, 1.5]]

    with patch("app.api.routes.predict_transaction") as mock_predict:
        mock_predict.side_effect = ValueError("Invalid probability")

        with TestClient(app, raise_server_exceptions=False) as client:
            response = client.post("/predict", json=transaction)
    assert response.status_code == 500

@pytest.mark.parametrize("probability", [1.5, -0.1, float("nan"), float("inf"), float("-inf")])
def test_invalid_probability_raises_error(probability):
    mock_model = Mock()

    mock_model.predict_proba.return_value = [[1 - probability, probability]]

    features = [0.0] * len(FEATURES)

    with pytest.raises(ValueError, match="invalid probability"):
        predict_transaction(mock_model, features)

@pytest.mark.parametrize(
    ("probability", "expected"),
    [
        (0.49, False),
        (0.50, True),
        (0.51, True),
    ],
)
def test_fraud_classification_uses_threshold(probability, expected):
    mock_model = Mock()
    mock_model.predict_proba.return_value = [
        [1 - probability, probability]
    ]

    features = [0.0] * len(FEATURES)

    result = predict_transaction(mock_model, features)

    assert result["is_fraud"] is expected
    assert result["fraud_probability"] == probability
    assert result["threshold"] == 0.5
