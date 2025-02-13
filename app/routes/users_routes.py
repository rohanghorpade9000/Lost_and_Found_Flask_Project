from flask import Blueprint, request, jsonify
from app.config import db
import bcrypt
import jwt
from datetime import datetime, timedelta
from app.jwt_token import SECRET_KEY


users_bp = Blueprint("users", __name__)


@users_bp.route("/users/login", methods=["POST"])
def login_user():
    """User login endpoint"""
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    # Fetch user from database
    user = db.users.find_one({"email": email})

    if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return jsonify({"error": "Invalid email or password."}), 401

    # Generate JWT token (valid for 24 hours)
    token = jwt.encode(
        {"email": email, "exp": datetime.utcnow() + timedelta(hours=24)},
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"message": "Login successful!", "token": token}), 200






@users_bp.route("/users/register", methods=["POST"])
def register_user():
    """User registration endpoint"""
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    # Check if user already exists
    if db.users.find_one({"email": email}):
        return jsonify({"error": "User already registered."}), 400

    # Hash the password before storing
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Store user in the database
    db.users.insert_one({"email": email, "password": hashed_password})

    return jsonify({"message": "User registered successfully!"}), 201
