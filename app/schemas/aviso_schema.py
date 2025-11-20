from marshmallow import Schema, fields


class AvisoSchema(Schema):
    titulo = fields.Str(required=True)
    conteudo = fields.Str(required=True)