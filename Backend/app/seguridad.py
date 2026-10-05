from functools import wraps

import jwt

from flask import request, jsonify, current_app


def _extraer_y_validar_token():

    """Extrae el token JWT, lo valida y devuelve el usuario_id."""

    auth_header = request.headers.get(
        "Authorization"
    )

    if not auth_header:

        return None, (
            jsonify({
                "success": False,
                "error": {
                    "message": "Token no proporcionado."
                }
            }),
            401
        )

    partes = auth_header.split()

    if (
        len(partes) != 2
        or partes[0].lower() != "bearer"
    ):

        return None, (
            jsonify({
                "success": False,
                "error": {
                    "message": (
                        "Formato de token inválido. "
                        "Use: Bearer <token>"
                    )
                }
            }),
            401
        )

    token = partes[1]

    try:

        payload = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )

        usuario_id = int(
            payload["sub"]
        )

        return usuario_id, None

    except jwt.ExpiredSignatureError:

        return None, (
            jsonify({
                "success": False,
                "error": {
                    "message": "Token expirado."
                }
            }),
            401
        )

    except jwt.InvalidTokenError:

        return None, (
            jsonify({
                "success": False,
                "error": {
                    "message": "Token inválido."
                }
            }),
            401
        )


def token_requerido(func):

    """Decorador que exige un token JWT válido."""

    @wraps(func)
    def decorador(*args, **kwargs):

        usuario_id, error = (
            _extraer_y_validar_token()
        )

        if error:

            return error

        return func(
            *args,
            usuario_id=usuario_id,
            **kwargs
        )

    return decorador


def admin_requerido(func):

    """
    Decorador que exige un token válido
    y que el usuario tenga rol de administrador.
    """

    @wraps(func)
    def decorador(*args, **kwargs):

        usuario_id, error = (
            _extraer_y_validar_token()
        )

        if error:

            return error

        from app.dominios.usuarios.repositorios import (
            UsuarioRepositorio
        )

        from app.dominios.usuarios.servicios import (
            PermisoDenegadoError
        )

        usuario = (
            UsuarioRepositorio.obtener_por_id(
                usuario_id
            )
        )

        if not usuario or usuario.rol != "admin":

            raise PermisoDenegadoError(
                "Permiso denegado. "
                "Se requiere rol de administrador."
            )

        return func(
            *args,
            usuario_id=usuario_id,
            **kwargs
        )

    return decorador