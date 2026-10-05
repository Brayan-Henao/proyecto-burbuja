from marshmallow import Schema, fields, validate


class RegistroUsuarioDTO(Schema):

    """DTO para validar el registro de usuarios."""

    correo = fields.Email(
        required=True
    )

    contrasena = fields.String(
        required=True,
        validate=validate.Length(min=6)
    )