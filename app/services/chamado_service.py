from app.models.chamado_model import Chamado
from app.schemas.chamado_schema import ChamadoSchema
from app import db
from datetime import datetime
from zoneinfo import ZoneInfo


class ChamadoService:

    @staticmethod
    def create(data, user):
        """
        Cria um novo chamado no sistema

        data = {
            "titulo": "",
            "descricao": "",
            "categoria": ""
        }
        """

        titulo = data.get("titulo")
        descricao = data.get("descricao")
        categoria = data.get("categoria")

        if not titulo or not descricao or not categoria:
            return {"error": "Título, categoria e descrição são obrigatórios"}, 400

        chamado = Chamado(
            titulo=titulo,
            categoria=categoria,
            descricao=descricao,
            status="aberto",
            data=datetime.now(ZoneInfo("America/Sao_Paulo")),
            autor_id=user.id,
            autor=user.nome_completo
        )

        db.session.add(chamado)
        db.session.commit()

        return {"message": "Chamado criado com sucesso", "id": chamado.id}, 201

    @staticmethod
    def listar(user):
        """
        Lista os chamados abertos ou em andamento
        """

        query = Chamado.query.filter(
            Chamado.status.in_(["aberto", "andamento"])
        )

        if user.tipo_usuario != "sindico":
            query = query.filter_by(autor_id=user.id)

        chamados = query.order_by(Chamado.data.desc()).all()

        schema = ChamadoSchema(many=True)
        return schema.dump(chamados), 200

    @staticmethod
    def detalhes(chamado_id):
        """
        Retorna os detalhes de um chamado específico.
        """

        chamado = db.session.get(Chamado, chamado_id)

        if not chamado:
            return {"error": "Chamado não encontrado"}, 404

        schema = ChamadoSchema()
        return schema.dump(chamado), 200

    @staticmethod
    def update_status(chamado_id, status, user):
        """
        Atualiza o status de um chamado existente.

        data = {
            "status": ""
        }
        """

        chamado = db.session.get(Chamado, chamado_id)

        if not chamado:
            return {"error": "Chamado não encontrado"}, 404

        if user.tipo_usuario != "sindico":
            return {"error": "Somente o síndico pode alterar o status"}, 403

        if status not in ["aberto", "andamento", "concluido"]:
            return {"error": "Status inválido"}, 400

        chamado.status = status
        db.session.commit()

        return {"message": "Status atualizado com sucesso"}, 200