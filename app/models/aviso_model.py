from app import db
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


class Aviso(db.Model):
    __tablename__ = "avisos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)

    autor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    autor = db.Column(db.String(150), nullable=False)

    data = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("America/Sao_Paulo")))
    editavel_ate = db.Column(
        db.DateTime,
        default=lambda: datetime.now(ZoneInfo("America/Sao_Paulo")) + timedelta(minutes=5)
    )

    ativo = db.Column(db.Boolean, default=True, nullable=False)

    usuario = db.relationship("User", backref="avisos")


    def __repr__(self):
        return f"<Aviso id={self.id} ativo={self.ativo}>"