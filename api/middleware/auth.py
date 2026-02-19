import jwt, os
from flask import request, jsonify
from functools import wraps

SECRET = os.getenv("JWT_SECRET")

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "token missing"}), 401
        try:
            jwt.decode(token.split()[1], SECRET, algorithms=["HS256"])
        except:
            return jsonify({"error": "invalid token"}), 401
        return f(*args, **kwargs)
    return wrapper
