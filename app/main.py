from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.ml.model_loader import load_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    app.state.model= load_model()
    yield

app= FastAPI(lifespan=lifespan)

@app.get("/health")
def health_check():
    model_loaded= getattr(app.state, "model", None) is not None
    return {"status": "healthy" if model_loaded else "unhealthy", "model_loaded": model_loaded}