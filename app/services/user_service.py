from werkzeug.security import generate_password_hash
from app.schemas.user_schema import UserSchema
from marshmallow import ValidationError
from app.models.user_model import User
from app import db
import re


class UserService:

    @staticmethod
    def create_user(data):
        """
        data = {
            "nome_completo": "",
            "email": "",
            "bloco_apto": "",
            "telefone": "",
            "tipo_usuario": "",
            "senha": ""
        }
        """

        # VALIDAÇÕES DE LÓGICA DE NEGÓCIO

        # Nome: mínimo 3 letras
        nome = data["nome_completo"].strip()
        if not re.match(r"^[A-Za-zÀ-ÿ\s]{3,}$", nome):
            return {"error": "Nome inválido: mínimo 3 letras"}, 400

        # Bloco/Apartamento: A/000
        if not re.match(r"^[A-Z]\/\d{1,3}$", data["bloco_apto"].strip()):
            return {"error": "Bloco/Apartamento inválido: use padrão A/000"}, 400

        # Telefone: mínimo 8 dígitos numéricos
        digits = re.sub(r"\D", "", data["telefone"])
        if len(digits) < 8:
            return {"error": "Telefone inválido: mínimo 8 dígitos"}, 400

        # E-mail não pode repetir
        if User.query.filter_by(email=data["email"].lower()).first():
            return {"error": "E-mail já cadastrado"}, 409

        # Senha: mínimo 6 caracteres
        if len(data["senha"]) < 6:
            return {"error": "Senha muito curta: mínimo 6 caracteres"}, 400

        # NORMALIZAÇÃO

        email_normalizado = data["email"].lower()

        # CRIAÇÃO DO USUÁRIO
        user = User(
            nome_completo=nome,
            email=email_normalizado,
            bloco_apto=data["bloco_apto"],
            telefone=data["telefone"],
            tipo_usuario=data["tipo_usuario"],
            senha_hash=generate_password_hash(data["senha"])
        )

        db.session.add(user)
        db.session.commit()

        return {"message": "Usuário cadastrado com sucesso"}, 201

    @staticmethod
    def update_user(user, data):
        """
        data = {
            "nome_completo": "",
            "email": "",
            "bloco_apto": "",
            "telefone": "",
            "senha": ""
        }

        AVISO: Não precisa passar todos os campos, apenas aqueles que vão ser atualizados.
        """

        schema = UserSchema(partial=True)

        try:
            validated = schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        if "nome_completo" in validated:
            nome = validated["nome_completo"].strip()
            if not re.match(r"^[A-Za-zÀ-ÿ\s]{3,}$", nome):
                return {"error": "Nome inválido: mínimo 3 letras"}, 400
            user.nome_completo = nome

        if "email" in validated:
            email = validated["email"].lower()
            if User.query.filter(User.email == email, User.id != user.id).first():
                return {"error": "E-mail já cadastrado"}, 409
            user.email = email

        if "bloco_apto" in validated:
            user.bloco_apto = validated["bloco_apto"]

        if "telefone" in validated:
            digits = re.sub(r"\D", "", validated["telefone"])
            if len(digits) < 8:
                return {"error": "Telefone inválido: mínimo 8 dígitos"}, 400
            user.telefone = validated["telefone"]

        if "senha" in validated:
            if len(validated["senha"]) < 6:
                return {"error": "Senha muito curta"}, 400
            user.senha_hash = generate_password_hash(validated["senha"])

        db.session.commit()
        return {"message": "Usuário atualizado com sucesso"}, 200