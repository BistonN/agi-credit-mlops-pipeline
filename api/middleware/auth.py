import jwt, os
from flask import request, jsonify
from functools import wraps

SECRET = os.getenv("JWT_SECRET", "agisecretkey")

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return jsonify({"error": "token missing"}), 401
        try:
            jwt.decode(auth.split()[1], SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "invalid token"}), 401
        return f(*args, **kwargs)
    return wrapper
