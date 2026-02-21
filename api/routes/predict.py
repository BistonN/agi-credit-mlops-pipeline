import os
import pandas as pd
from flask import Blueprint, request, jsonify
from rpy2 import robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import default_converter

from middleware.auth import token_required
from middleware.schema_validator import validate_payload
from middleware.model_loader import get_model_path, get_latest_version

predict_bp = Blueprint("predict", __name__)

robjects.r("library(tidymodels)")

readRDS = robjects.r["readRDS"]
predict_tm = robjects.r["predict"]

@predict_bp.route("/predict", methods=["POST"])
@token_required
def predict():
    version = request.args.get("version") or get_latest_version()

    model_path = get_model_path(version)

    if not os.path.exists(model_path):
        return jsonify({"error": "model version not found"}), 404

    model = readRDS(model_path)

    data = request.get_json()

    err = validate_payload(data, version)
    if err:
        return jsonify({"error": err}), 400

    df = pd.DataFrame([data])

    with localconverter(default_converter + pandas2ri.converter):
        r_df = robjects.conversion.py2rpy(df)

    probs = predict_tm(model, r_df, type="prob")

    prob_default = float(probs.rx2(".pred_1")[0])
    prediction = int(prob_default >= 0.5)

    return jsonify({
        "model_version": version,
        "prediction": prediction,
        "prob_default": prob_default
    })