import math

import pandas as pd

from app.core.config import FRAUD_THRESHOLD
from app.api.schemas import FEATURES

def predict_transaction(model, features):
    transaction = pd.DataFrame([features], columns=FEATURES)
    probability= float(model.predict_proba(transaction)[0][1])

    if not math.isfinite(probability) or not 0 <= probability <= 1:
        raise ValueError("Model returned an invalid probability")
    return {
        "fraud_probability": probability,
        "is_fraud": probability >= FRAUD_THRESHOLD,
        "threshold": FRAUD_THRESHOLD
    }