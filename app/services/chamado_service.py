from app.models.chamado_model import Chamado
from app import db
from datetime import datetime
from zoneinfo import ZoneInfo


class ChamadoService:

    @staticmethod
    def create(data, user):
        chamado = Chamado(
            titulo=data["titulo"],
            categoria=data["categoria"],
            descricao=data["descricao"],
            autor_id=user.id,
            autor=user.nome_completo,
            status="aberto",
            data=datetime.now(ZoneInfo("America/Sao_Paulo")),
        )

        db.session.add(chamado)
        db.session.commit()

        return {"message": "Chamado criado com sucesso", "id": chamado.id}, 201