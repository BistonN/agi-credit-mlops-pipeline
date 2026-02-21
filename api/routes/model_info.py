import json, os
from flask import Blueprint, jsonify, request
from middleware.auth import token_required
from middleware.model_loader import load_metadata

model_info_bp = Blueprint("model_info", __name__)

@model_info_bp.route("/model-info", methods=["GET"])
@token_required
def model_info():
    version = request.args.get("version")

    if not os.path.exists("/app/artifacts/metadata.json"):
        return jsonify({"error": "model metadata not found"}), 404

    meta = load_metadata()

    if not version:
        return jsonify(meta)

    for m in meta["models"]:
        if m["version"] == version:
            return jsonify(m)

    return jsonify({"error": "model version not found"}), 404