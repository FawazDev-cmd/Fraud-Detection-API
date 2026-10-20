from fastapi import APIRouter, Request

from app.api.schemas import FEATURES, PredictionResponse, TransactionRequest
from app.services.prediction_service import predict_transaction

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict(payload: TransactionRequest, request: Request):
    features = [getattr(payload, name) for name in FEATURES]
    model= request.app.state.model
    return predict_transaction(model, features)