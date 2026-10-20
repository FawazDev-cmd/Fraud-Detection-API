import joblib
from pathlib import Path

MODEL_PATH= (
    Path(__file__).resolve().parents[2] / "artifacts" / "fraud_pipeline.joblib"
)

def load_model():
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)