from enum import Enum

import uvicorn
import xgboost
from fastapi import FastAPI

from .classifiers.preprocess import PydanticOneHotEncoder
from .models import DatasetName, RequestParamModel, get_request_model

app = FastAPI()


class ModelName(str, Enum):
    xgboost = "xgboost"
    tabpfn = "tabpfn"


@app.post("/transform_request/{dataset_name}")
async def transform_request(
    dataset_name: DatasetName, request_params: RequestParamModel
):
    encoder = PydanticOneHotEncoder(get_request_model(dataset_name))
    encoded_request = encoder.transform([request_params])
    return {
        "dataset_name": dataset_name,
        "encoded_request": encoded_request.to_dict(orient="records")[0],
    }


@app.post("/classify/{dataset_name}")
async def classify(
    dataset_name: DatasetName,
    request_params: RequestParamModel,
    model_name: ModelName = ModelName.xgboost,
):
    encoder = PydanticOneHotEncoder(get_request_model(dataset_name))
    df = encoder.transform([request_params])
    if model_name == ModelName.xgboost:
        model = xgboost.XGBClassifier()
    else:
        raise ValueError(f"Unsupported model: {model_name}")
    # Will raise an error as the model is not trained
    predictions = model.predict(df)
    return {
        "dataset_name": dataset_name,
        "model_name": model_name,
        "predictions": predictions.tolist(),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
