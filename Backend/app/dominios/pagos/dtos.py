from marshmallow import Schema, fields


class CrearPagoDTO(Schema):

    orden_id = fields.Integer(
        required=True
    )