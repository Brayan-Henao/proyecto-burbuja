from flask import Blueprint, request, jsonify

from marshmallow import ValidationError

from app.dominios.usuarios.dtos import (
    RegistroUsuarioDTO
)

from app.dominios.usuarios.servicios import (
    CorreoYaRegistradoError,
    CredencialesInvalidasError
)

from app.seguridad import (
    token_requerido,
    admin_requerido
)


usuarios_bp = Blueprint(
    "usuarios",
    __name__
)

admin_bp = Blueprint(
    "admin",
    __name__
)


# Variable que recibirá el servicio de usuarios
usuario_servicio = None


# ==========================================
# RUTAS DE USUARIOS
# ==========================================

@usuarios_bp.route(
    "/registro",
    methods=["POST"]
)
def registro():

    datos = request.get_json(
        silent=True
    ) or {}

    dto = RegistroUsuarioDTO()

    try:

        datos_validados = dto.load(
            datos
        )

    except ValidationError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": "Datos de entrada inválidos.",
                "details": err.messages
            }
        }), 400

    try:

        usuario = usuario_servicio.registrar_usuario(
            datos_validados
        )

    except CorreoYaRegistradoError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 409

    return jsonify({
        "success": True,
        "message": "Usuario creado con éxito.",
        "data": {
            "id": usuario.id,
            "correo": usuario.correo
        }
    }), 201


@usuarios_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    datos = request.get_json(
        silent=True
    ) or {}

    if not datos.get("correo") or not datos.get(
        "contrasena"
    ):

        return jsonify({
            "success": False,
            "error": {
                "message": (
                    "Correo y contraseña son obligatorios."
                )
            }
        }), 400

    try:

        resultado = usuario_servicio.iniciar_sesion(
            datos
        )

    except CredencialesInvalidasError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 401

    return jsonify({
        "success": True,
        "message": "Inicio de sesión exitoso.",
        "data": resultado
    }), 200


# ==========================================
# RUTAS DE ADMINISTRACIÓN
# ==========================================

@admin_bp.route(
    "/usuarios",
    methods=["GET"]
)
@admin_requerido
def listar_usuarios(usuario_id):

    lista = usuario_servicio.listar_todos_los_usuarios()

    return jsonify({
        "success": True,
        "message": "Lista de usuarios.",
        "data": lista
    }), 200
