from app.models.aviso_model import Aviso
from app import db
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


class AvisoService:

    @staticmethod
    def create(data, user):
        aviso = Aviso(
            titulo=data["titulo"],
            conteudo=data["conteudo"],
            autor_id=user.id,
            autor=user.nome_completo,
            data=datetime.now(ZoneInfo("America/Sao_Paulo")),
            editavel_ate=datetime.now(ZoneInfo("America/Sao_Paulo")) + timedelta(minutes=5),
            ativo=True
        )

        db.session.add(aviso)
        db.session.commit()

        return {"message": "Aviso criado com sucesso", "id": aviso.id}, 201