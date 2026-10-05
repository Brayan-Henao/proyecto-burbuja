from marshmallow import Schema, fields, validate


class CrearOrdenItemDTO(Schema):

    producto_id = fields.Integer(
        required=True
    )

    personalizacion_id = fields.Integer(
        required=False,
        allow_none=True
    )

    cantidad = fields.Integer(
        required=False,
        load_default=1,
        validate=validate.Range(min=1)
    )


class CrearOrdenDTO(Schema):

    items = fields.List(
        fields.Nested(CrearOrdenItemDTO),
        required=True,
        validate=validate.Length(min=1)
    )