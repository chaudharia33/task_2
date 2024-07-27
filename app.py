from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI()

class PredictionRequest(BaseModel):
    year: int
    month: int
    stateDescription: str
    sectorName: str

@app.post("/predict")
async def predict(request: PredictionRequest):
    # Load the saved pickle file
    model = pickle.load(open("../model/model.pkl", "rb"))

    # Create a pandas dataframe from the user input
    data = pd.DataFrame({
        "year": [request.year],
        "month": [request.month],
        "stateDescription": [request.stateDescription],
        "sectorName": [request.sectorName]
    })

    # Make the prediction using the loaded model
    prediction = model.predict(data)

    return {"prediction": prediction.tolist()}