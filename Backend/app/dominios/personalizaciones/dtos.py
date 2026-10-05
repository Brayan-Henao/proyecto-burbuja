from marshmallow import Schema, fields, validate


class CrearPersonalizacionDTO(Schema):

    producto_id = fields.Integer(
        required=True
    )

    grabado = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(
            min=1,
            max=500
        )
    )

    mensaje = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(
            min=1,
            max=1000
        )
    )


class ActualizarPersonalizacionDTO(Schema):

    grabado = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(
            min=1,
            max=500
        )
    )

    mensaje = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(
            min=1,
            max=1000
        )
    )


class AgregarFotoPersonalizacionDTO(Schema):

    url_imagen = fields.String(
        required=True,
        validate=validate.Length(
            min=1,
            max=500
        )
    )

    orden = fields.Integer(
        required=False,
        validate=validate.Range(
            min=1
        )
    )


class AgregarOpcionPersonalizacionDTO(Schema):

    opcion_producto_id = fields.Integer(
        required=True
    )