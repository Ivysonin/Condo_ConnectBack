from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.services.auth_service import AuthService


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON não enviado"}), 400

    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    response, status = AuthService.login(email, senha)
    return jsonify(response), status


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout_user():
    response, status = AuthService.logout()
    return jsonify(response), status