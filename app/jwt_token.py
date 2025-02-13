import jwt
import os
from functools import wraps
from flask import request, jsonify

SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret")

def token_required(f):
    """Decorator to verify JWT token before allowing access to protected routes."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            token = token.split(" ")[1]  # Extract token after "Bearer"
            decoded_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_email = decoded_data["email"]  # Attach email to request
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401

        return f(*args, **kwargs)

    return decorated
