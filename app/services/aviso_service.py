from app.models.aviso_model import Aviso
from app import db
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from app.schemas.aviso_schema import AvisoSchema


class AvisoService:

    @staticmethod
    def create(data, user):
        """
        Cria um novo aviso
        """

        agora = datetime.now(ZoneInfo("America/Sao_Paulo"))
        titulo = data.get("titulo")
        conteudo = data.get("conteudo")

        if not titulo or not conteudo:
            return {"error": "Título e conteúdo são obrigatórios"}, 400

        aviso = Aviso(
            titulo=titulo,
            conteudo=conteudo,
            autor_id=user.id,
            autor=user.nome_completo,
            data=agora,
            editavel_ate=agora + timedelta(minutes=5),
            ativo=True
        )

        db.session.add(aviso)
        db.session.commit()

        return {"message": "Aviso criado com sucesso", "id": aviso.id}, 201
    
    @staticmethod
    def exibir():
        """
        exibir os avisos ativos
        """

        avisos = (
            Aviso.query
            .filter_by(ativo=True)
            .order_by(Aviso.data.desc())
            .all()
        )

        schema = AvisoSchema(many=True)
        return schema.dump(avisos), 200

    @staticmethod
    def edit(aviso_id, data, user):
        """
        edita um aviso dentro do prazo de 5 minutos
        """

        aviso = db.session.get(Aviso, aviso_id)

        if not aviso or not aviso.ativo:
            return {"error": "Aviso não encontrado"}, 404

        # Só o próprio autor pode editar
        if aviso.autor_id != user.id:
            return {"error": "Você não tem permissão para editar este aviso"}, 403

        agora = datetime.now(ZoneInfo("America/Sao_Paulo"))

        # Verifica se ainda está no prazo de edição
        if agora > aviso.editavel_ate:
            return {"error": "Tempo de edição expirado"}, 403

        aviso.titulo = data.get("titulo", aviso.titulo)
        aviso.conteudo = data.get("conteudo", aviso.conteudo)

        db.session.commit()

        return {"message": "Aviso atualizado com sucesso"}, 200

    @staticmethod
    def delete(aviso_id, user):
        """
        deleta um aviso(deixa o mesmo desativado)
        """

        aviso = db.session.get(Aviso, aviso_id)

        if not aviso or not aviso.ativo:
            return {"error": "Aviso não encontrado"}, 404

        # Só o síndico pode desativar
        if aviso.autor_id != user.id and user.tipo_usuario != "sindico":
            return {"error": "Você não tem permissão para remover este aviso"}, 403

        aviso.ativo = False

        db.session.commit()

        return {"message": "Aviso desativado com sucesso"}, 200