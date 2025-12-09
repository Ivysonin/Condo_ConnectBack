from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models.user_model import User
from app.schemas.user_schema import UserSchema


admin_bp = Blueprint("admin", __name__)
schema = UserSchema(many=True)


@admin_bp.route("/usuarios", methods=["GET"])
@login_required
def listar_usuarios_admin():

    if current_user.tipo_usuario != "sindico":
        return jsonify({"error": "Acesso permitido apenas ao síndico"}), 403

    usuarios = User.query.order_by(User.id.desc()).all()
    return jsonify(schema.dump(usuarios)), 200