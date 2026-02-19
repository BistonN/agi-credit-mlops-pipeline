import json, jwt, datetime, os
from flask import Blueprint, request, jsonify
from pathlib import Path

SECRET = os.getenv("JWT_SECRET")

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    
    BASE_DIR = Path(__file__).resolve().parent.parent
    USERS_FILE = BASE_DIR / "data" / "users.json"

    users = json.load(open(USERS_FILE))
    
    user = next((u for u in users if u["username"]==data["username"] and u["password"]==data["password"]), None)
    if not user:
        return jsonify({"error": "invalid credentials"}), 401
    token = jwt.encode(
        {"user": user["username"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET,
        algorithm="HS256"
    )
    return jsonify({"token": token})
