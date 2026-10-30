from pathlib import Path
import warnings
from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import numpy as np

try:
    import pandas as pd
except ImportError:
    pd = None

app = FastAPI(
    title="Sales Prediction API",
    description="Predict Sales based on Advertising Budget",
    version="1.0.0"
)

# Load the trained model
model_path = Path(__file__).parent / "sales.pkl"
model = joblib.load(model_path)


class SalesInput(BaseModel):
    AdvertisingBudget: float = Field(..., description="Advertising budget in dollars", ge=0, example=456.0)


# API endpoints

@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "message": "Sales Prediction API is running"
    }


@app.post("/predict")
def predict_sales(payload: SalesInput):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if pd is not None:
            input_data = pd.DataFrame([{"AdvertisingBudget": payload.AdvertisingBudget}])
        else:
            input_data = np.array([[payload.AdvertisingBudget]])
        prediction = model.predict(input_data)

    predicted_sales = round(float(prediction[0]), 2)

    return {
        "AdvertisingBudget": payload.AdvertisingBudget,
        "predicted_sales": predicted_sales
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fsales_api:app", host="127.0.0.1", port=8000, reload=True)
