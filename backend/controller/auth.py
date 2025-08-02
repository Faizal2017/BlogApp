from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from models.user_model import create_user, find_user_by_email, check_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    db = current_app.db

    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Missing fields"}), 400

    if find_user_by_email(db, data["email"]):
        return jsonify({"message": "Email already registered"}), 409

    create_user(db, data["username"], data["email"], data["password"])
    return jsonify({"message": "Registration successful"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    db = current_app.db

    if not data.get("email") or not data.get("password"):
        return jsonify({"message": "Missing credentials"}), 400

    user = find_user_by_email(db, data["email"])
    if not user or not check_password(user, data["password"]):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity=str(user["_id"]))
    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "username": user["username"],
        "email": user["email"]
    }), 200
