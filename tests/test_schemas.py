import pytest
from pydantic import ValidationError

from app.api.schemas import FEATURES, TransactionRequest


@pytest.fixture
def valid_transaction():
    return {feature: 0.0 for feature in FEATURES}


def test_valid_transaction(valid_transaction):
    transaction = TransactionRequest(**valid_transaction)

    assert set(transaction.model_dump().keys()) == set(FEATURES)


def test_missing_feature(valid_transaction):
    valid_transaction.pop("V1")

    with pytest.raises(ValidationError):
        TransactionRequest(**valid_transaction)


def test_extra_field(valid_transaction):
    valid_transaction["Class"] = 0

    with pytest.raises(ValidationError):
        TransactionRequest(**valid_transaction)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_value(valid_transaction, value):
    valid_transaction["V1"] = value

    with pytest.raises(ValidationError):
        TransactionRequest(**valid_transaction)


def test_negative_amount(valid_transaction):
    valid_transaction["Amount"] = -1.0

    with pytest.raises(ValidationError):
        TransactionRequest(**valid_transaction)
