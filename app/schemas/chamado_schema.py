from marshmallow import Schema, fields


class ChamadoSchema(Schema):
    titulo = fields.Str(required=True)
    categoria = fields.Str(required=True)
    descricao = fields.Str(required=True)