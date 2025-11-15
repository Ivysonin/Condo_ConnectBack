from flask import Blueprint, request, jsonify
from app.schemas.user_schema import UserSchema
from app.services.user_service import UserService


user_bp = Blueprint("user", __name__)
schema = UserSchema()


@user_bp.route("/register", methods=["POST"])
def register_user():

    # Valida estrutura(schema)
    json_data = request.get_json()

    if not json_data:
        return jsonify({"error": "JSON não enviado"}), 400

    errors = schema.validate(json_data)
    if errors:
        return jsonify(errors), 400

    # Carregar dados validados
    data = schema.load(json_data)

    # Passar para o service (regras de negócio + criação)
    response, status = UserService.create_user(data)

    return jsonify(response), status