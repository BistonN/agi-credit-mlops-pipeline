import os
import json
from flask import Blueprint, jsonify

model_info_bp = Blueprint("model_info", __name__)

METADATA_PATH = os.getenv("MODEL_METADATA_PATH", "/app/artifacts/model_metadata.json")

@model_info_bp.route("/model-info", methods=["GET"])
def model_info():
    if not os.path.exists(METADATA_PATH):
        return jsonify({"error": "model metadata not found"}), 404

    with open(METADATA_PATH, "r") as f:
        metadata = json.load(f)

    return jsonify(metadata)