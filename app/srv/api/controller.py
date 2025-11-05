from fastapi import APIRouter, HTTPException
from typing import Any
import joblib

from .dto import PredictionInput
from app.config.paths_config import MODEL_OUTPUT_PATH

model = joblib.load(MODEL_OUTPUT_PATH)

router = APIRouter(prefix="/api", tags=["Prediction"])

@router.post("/predict")
def predict(payload: PredictionInput) -> Any:
    try:
        X_input = payload.to_numpy()
        
        prediction = model.predict(X_input).tolist()[0]

        prediction = "Valid" if prediction == 1 else "Invalid"

        return {"prediction": prediction}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
