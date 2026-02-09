from flask import Blueprint, request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, set_access_cookies, set_refresh_cookies)
from pydantic import ValidationError
from datetime import timedelta
from Models.model import LoginRequest, SignupRequest
from Database.DatabaseOperations import DatabaseOperations as db_ops

login_bp = Blueprint("auth", __name__)

def parse_body(model, data):

    try:
        return model.model_validate(data), None
    
    except ValidationError as e:
        return None, e.errors()
@login_bp.route("/signup", methods=["POST"])
def signup():
    # body, error = parse_body(SignupRequest, request.json)
    # if error:
    #     return jsonify({"success": False, "errors": error}), 400
    data = request.get_json()

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")
    
    add_user = db_ops.add_user(first_name, last_name, email, password)
    if add_user:
        return jsonify({"message": "User added", "User Name": first_name}), 201

@login_bp.route("/login", methods=["POST"])
def login():
    # body, error = parse_body(LoginRequest, request.json)
    # if error:
    #     return jsonify({"success": False, "errors": error}), 400
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    credntials_valid = db_ops.check_credentials(email, password)
    if not credntials_valid:
        return jsonify({"error": "Invalid email or password"}), 401
    
    access_token = create_access_token(identity=email, expires_delta=timedelta(minutes=12))
    refresh_token = create_refresh_token(identity=email, expires_delta=timedelta(days=7))

    response = jsonify({"access_token": access_token, "refresh_token": refresh_token})
    # response = jsonify({"success": True})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return (response, 200)

@login_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    
    refresh_identity = get_jwt_identity()

    if not refresh_identity:
        return jsonify({"error": "Missing refresh token"}), 401

    # try:
    #     payload = get_jwt()

    # except Exception as e:
    #     print("DECODE ERROR:", e)
    #     return jsonify({"error": "Invalid refresh token"}), 401

    # if payload["type"] != "refresh":
    #     raise Exception("Invalid token type")

    new_access_token = create_access_token(identity=refresh_identity, expires_delta=timedelta(minutes=10))
    new_refresh_token = create_refresh_token(identity=refresh_identity, expires_delta=timedelta(days=7))

    # response = jsonify({"access_token": new_access_token, "refresh_token": new_refresh_token})
    response = jsonify({"success": True})
    set_access_cookies(response, new_access_token)
    set_refresh_cookies(response, new_refresh_token)

    return response

@login_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_users():
    get_all_users
    pass
    users = db_ops.get_all_users()
    return jsonify([
        {"First Name": user.first_name , "Last Name": user.last_name, "Email": user.email, "Password": user.password}
        for user in users])

@login_bp.route("/", methods=["DELETE"])
@jwt_required()
def delete_user():
    email = request.get_json().get("email")

    if not email:
        return jsonify({"error": "Product email required"}), 400

    deleted = db_ops.delete_user(email)
    
    if deleted:
        return jsonify({"message": "User deleted", "User email": email}), 200

    else:
        return jsonify({"error": "User not found"}), 404
