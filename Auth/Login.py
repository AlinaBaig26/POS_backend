from flask import Blueprint, request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, set_access_cookies, set_refresh_cookies)
from pydantic import ValidationError
from datetime import timedelta
from Models.model import LoginRequest
from Database.DatabaseOperations import DatabaseOperations as db_ops

login_bp = Blueprint("auth", __name__)

def parse_body(model, contacts):

    try:
        return model.model_validate(contacts), None
    
    except ValidationError as e:
        return None, e.errors()

@login_bp.route("/login", methods=["POST"])
def login():
    body, error = parse_body(LoginRequest, request.json)
    if error:
        return jsonify({"success": False, "errors": error}), 400

    credntials_valid = db_ops.check_credentials(body.name, body.password)
    if not credntials_valid:
        return jsonify({"error": "Invalid name or password"}), 401
    
    access_token = create_access_token(identity=body.name, expires_delta=timedelta(minutes=12))
    refresh_token = create_refresh_token(identity=body.name, expires_delta=timedelta(days=7))

    # response = jsonify({"access_token": access_token, "refresh_token": refresh_token})
    response = jsonify({"success": True})
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
