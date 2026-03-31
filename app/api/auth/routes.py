from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies
)
from pydantic import ValidationError
# from datetime import timedelta
from .schemas import LoginRequest, SignupRequest
from .repository import AuthRepository as AR
from .service import AuthService
from app.api.constants import parse_body

login_bp = Blueprint("auth", __name__)
service = AuthService()

from flask import jsonify, request

@login_bp.route("/signup", methods=["POST"])
def signup():
    payload = request.get_json(silent=True) or {}

    body, error = parse_body(SignupRequest, payload)
    if error:
        return jsonify({
            "success": False,
            "message": "Validation failed.",
            "errors": error,
        }), 400

    try:
        service.signup(
            first_name=body.first_name,
            last_name=body.last_name,
            email=body.email,
            password=body.password,
        )
        return jsonify({
            "success": True,
            "message": "User account created successfully.",
        }), 201

    except ValueError as e:
        # Use ValueError for expected business-rule conflicts (e.g., email already exists)
        return jsonify({
            "success": False,
            "message": "Request could not be completed.",
            "error": str(e),
        }), 409

    except Exception:
        # Don’t leak internals to clients
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred.",
        }), 500



@login_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json(silent=True) or {}
    body, error = parse_body(LoginRequest, payload)
    if error:
        return jsonify({"success": False, "errors": error}), 400
    
    tokens = service.login(body.email, body.password)
    if not tokens:
        return jsonify({"error": "Invalid email or password"}), 401

    response = jsonify(tokens)  # or jsonify({"success": True})
    set_access_cookies(response, tokens["access_token"])
    set_refresh_cookies(response, tokens["refresh_token"])
    return response, 200

@login_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():

    refresh_identity = get_jwt_identity()

    if not refresh_identity:
        return jsonify({"error": "Missing refresh token"}), 401

    tokens = service.refreshTokens(refresh_identity)

    response = jsonify(tokens)  # or jsonify({"success": True})
    set_access_cookies(response, tokens["access_token"])
    set_refresh_cookies(response, tokens["refresh_token"])
    return response, 200

@login_bp.route("/", methods=["GET"])
@jwt_required()
def getAllUsers():
    users = service.listUsers()
    return jsonify(
        [
            {
                "First Name": user.first_name,
                "Last Name": user.last_name,
                "Email": user.email,
                "Password": user.password,
            }
            for user in users
        ]
    )


@login_bp.route("/", methods=["DELETE"])
@jwt_required()
def deleteUser():
    data = request.get_json(silent=True) or {}
    email = data.get("email")

    if not email:
        return jsonify({"error": "Product email required"}), 400

    deleted = service.deleteUser(email)

    if deleted:
        return jsonify({"message": "User deleted", "User email": email}), 200

    else:
        return jsonify({"error": "User not found"}), 404
