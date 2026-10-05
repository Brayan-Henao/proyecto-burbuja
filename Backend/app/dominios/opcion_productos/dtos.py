from marshmallow import Schema, fields, validate


class CrearOpcionProductoDTO(Schema):
    producto_id = fields.Integer(required=True)
    tipo = fields.String(required=True, validate=validate.Length(min=1, max=50))
    valor = fields.String(required=True, validate=validate.Length(min=1, max=100))
    activa = fields.Boolean(required=False)
    opcion_principal_id = fields.Integer(required=False, allow_none=True)


class ActualizarOpcionProductoDTO(Schema):
    tipo = fields.String(required=True, validate=validate.Length(min=1, max=50))
    valor = fields.String(required=True, validate=validate.Length(min=1, max=100))
    activa = fields.Boolean(required=True)
    opcion_principal_id = fields.Integer(required=False, allow_none=True)