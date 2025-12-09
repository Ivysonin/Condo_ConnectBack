from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from marshmallow import ValidationError
from app.services.chamado_service import ChamadoService
from app.schemas.chamado_schema import ChamadoSchema


chamado_bp = Blueprint("chamado", __name__)
schema = ChamadoSchema()


@chamado_bp.route("/", methods=["GET"])
@login_required
def listar_chamados():
    response, status = ChamadoService.listar(current_user)
    return jsonify(response), status


@chamado_bp.route("/<int:chamado_id>", methods=["GET"])
@login_required
def detalhes_chamado(chamado_id):
    response, status = ChamadoService.detalhes(chamado_id)
    return jsonify(response), status


@chamado_bp.route("/", methods=["POST"])
@login_required
def criar_chamado():

    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "JSON não enviado"}), 400

    try:
        data = schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    response, status = ChamadoService.create(data, current_user)
    return jsonify(response), status


@chamado_bp.route("/<int:chamado_id>", methods=["PATCH"])
@login_required
def update_status_chamado(chamado_id):

    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "JSON não enviado"}), 400
    
    status_novo = json_data.get("status")

    response, status = ChamadoService.update_status(chamado_id, status_novo, current_user)
    return jsonify(response), status