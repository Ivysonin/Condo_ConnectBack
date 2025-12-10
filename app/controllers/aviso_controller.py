from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from marshmallow import ValidationError
from app.services.aviso_service import AvisoService
from app.schemas.aviso_schema import AvisoSchema


aviso_bp = Blueprint("aviso", __name__)
schema = AvisoSchema()


@aviso_bp.route("/", methods=["GET"])
@login_required
def listar_avisos():
    response, status = AvisoService.exibir()
    return jsonify(response), status


@aviso_bp.route("/", methods=["POST"])
@login_required
def criar_aviso():

    if current_user.tipo_usuario != "sindico":
        return jsonify({"error": "Apenas o síndico pode criar avisos"}), 403

    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "JSON não enviado"}), 400

    try:
        data = schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    response, status = AvisoService.create(data, current_user)
    return jsonify(response), status


@aviso_bp.route("/<int:aviso_id>", methods=["PUT"])
@login_required
def editar_aviso(aviso_id):

    if current_user.tipo_usuario != "sindico":
        return jsonify({"error": "Apenas o síndico pode editar avisos"}), 403

    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "JSON não enviado"}), 400

    schema_partial = AvisoSchema(partial=True)

    try:
        data = schema_partial.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    response, status = AvisoService.edit(aviso_id, data, current_user)
    return jsonify(response), status


@aviso_bp.route("/<int:aviso_id>", methods=["DELETE"])
@login_required
def deletar_aviso(aviso_id):

    if current_user.tipo_usuario != "sindico":
        return jsonify({"error": "Apenas o síndico pode remover avisos"}), 403

    response, status = AvisoService.delete(aviso_id, current_user)
    return jsonify(response), status