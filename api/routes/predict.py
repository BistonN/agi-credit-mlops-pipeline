import os
import pandas as pd
import pyreadr
from flask import Blueprint, request, jsonify

predict_bp = Blueprint("predict", __name__)

env = os.getenv("ENV", "prod")

if env == "dev":
    model_path = "../../training/artifacts/model_v1.rds"
else:
    model_path = os.getenv("MODEL_PATH", "/app/artifacts/model_v1.rds")

model_object = pyreadr.read_r(model_path)
model = list(model_object.values())[0]

@predict_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    df = pd.DataFrame([data])

    probs = model.predict_proba(df)
    prob_default = float(probs[0][1])
    prediction = int(prob_default >= 0.5)

    return jsonify({
        "prediction": prediction,
        "prob_default": prob_default
    })
