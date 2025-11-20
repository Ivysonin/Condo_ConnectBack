from app import db
from datetime import datetime
from zoneinfo import ZoneInfo


class Chamado(db.Model):
    __tablename__ = "chamados"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="aberto", nullable=False)

    data = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("America/Sao_Paulo")))

    autor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    autor = db.Column(db.String(150), nullable=False)

    usuario = db.relationship("User", backref="chamados")


    def __repr__(self):
        return f"<Chamado id={self.id}>"