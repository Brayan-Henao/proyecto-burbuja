from marshmallow import Schema, fields, validate


class CrearProductoDTO(Schema):

    """DTO para validar la creación de productos."""

    nombre = fields.String(
        required=True
    )

    descripcion = fields.String(
        required=True
    )

    precio = fields.Decimal(
        required=True,
        as_string=True
    )

    stock = fields.Integer(
        required=True,
        validate=validate.Range(min=0)
    )

    disponible = fields.Boolean(
        required=False
    )

    categoria = fields.String(
        required=True
    )

    min_fotos = fields.Integer(
        required=False,
        validate=validate.Range(min=1)
    )

    max_fotos = fields.Integer(
        required=False,
        validate=validate.Range(min=1)
    )

    permite_grabado = fields.Boolean(
        required=False
    )

    max_caracteres_grabado = fields.Integer(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1)
    )

    precio_grabado = fields.Decimal(
        required=False,
        as_string=True,
        validate=validate.Range(min=0)
    )

    permite_tarjeta = fields.Boolean(
        required=False
    )

    max_caracteres_tarjeta = fields.Integer(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1)
    )


class ActualizarProductoDTO(Schema):

    """DTO para validar la actualización de productos."""

    nombre = fields.String(
        required=True
    )

    descripcion = fields.String(
        required=True
    )

    precio = fields.Decimal(
        required=True,
        as_string=True
    )

    stock = fields.Integer(
        required=True,
        validate=validate.Range(min=0)
    )

    disponible = fields.Boolean(
        required=True
    )

    categoria = fields.String(
        required=True
    )

    min_fotos = fields.Integer(
        required=True,
        validate=validate.Range(min=1)
    )

    max_fotos = fields.Integer(
        required=True,
        validate=validate.Range(min=1)
    )

    permite_grabado = fields.Boolean(
        required=True
    )

    max_caracteres_grabado = fields.Integer(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1)
    )

    precio_grabado = fields.Decimal(
        required=False,
        as_string=True,
        validate=validate.Range(min=0)
    )

    permite_tarjeta = fields.Boolean(
        required=True
    )

    max_caracteres_tarjeta = fields.Integer(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1)
    )