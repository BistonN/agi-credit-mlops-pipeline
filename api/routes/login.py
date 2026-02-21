from flask import Blueprint, request, jsonify
import json, jwt, datetime, os
from pathlib import Path

login_bp = Blueprint("login", __name__)
SECRET = os.getenv("JWT_SECRET")

BASE_DIR = Path(__file__).resolve().parent.parent
USERS_FILE = BASE_DIR / "data" / "users.json"

def validate_login(data):
    if not isinstance(data, dict):
        return "invalid body"
    if not data.get("username"):
        return "username required"
    if not data.get("password"):
        return "password required"
    return None

@login_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    err = validate_login(data)
    if err:
        return jsonify({"error": err}), 400

    users = json.load(open(USERS_FILE))
    user = next(
        (u for u in users if u["username"] == data["username"] and u["password"] == data["password"]),
        None
    )

    if not user:
        return jsonify({"error": "invalid credentials"}), 401

    token = jwt.encode(
        {"user": user["username"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET,
        algorithm="HS256"
    )

    return jsonify({"token": token})
