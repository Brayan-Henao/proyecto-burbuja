from datetime import datetime, timedelta, timezone

import jwt

from flask import current_app

from werkzeug.security import generate_password_hash, check_password_hash

from app.dominios.usuarios.modelos import Usuario

from app.dominios.usuarios.repositorios import UsuarioRepositorio

class CorreoYaRegistradoError(Exception):
    pass


class CredencialesInvalidasError(Exception):
    pass


class UsuarioNoEncontradoError(Exception):
    pass


class PermisoDenegadoError(Exception):
    pass


# --- Función auxiliar de JWT ---

def _generar_access_token(usuario, secret_key, exp_minutes):

    """Genera un JWT de acceso con información básica."""

    ahora = datetime.now(timezone.utc)

    payload = {
        "sub": str(usuario.id),
        "iat": ahora,
        "exp": ahora + timedelta(minutes=exp_minutes),
    }

    token = jwt.encode(
        payload,
        secret_key,
        algorithm="HS256"
    )

    return token


class UsuarioServicio:

    """Lógica de negocio para la gestión de usuarios."""

    def __init__(self, secret_key, jwt_exp_minutes):

        self.secret_key = secret_key
        self.jwt_exp_minutes = jwt_exp_minutes


    def registrar_usuario(self, datos):

        """Registra un nuevo usuario con correo y contraseña protegida."""

        correo = datos["correo"]
        contrasena = datos["contrasena"]

        usuario_existente = (
            UsuarioRepositorio.obtener_por_correo(correo)
        )

        if usuario_existente:

            raise CorreoYaRegistradoError(
                f"El correo {correo} ya está registrado."
            )

        contrasena_hash = generate_password_hash(
            contrasena
        )

        usuario = Usuario(
            correo=correo,
            contrasena=contrasena_hash
        )

        UsuarioRepositorio.crear(usuario)

        return usuario


    def iniciar_sesion(self, datos):

        """Valida las credenciales y genera un JWT de acceso."""

        correo = datos.get("correo")
        contrasena = datos.get("contrasena")

        if not correo or not contrasena:

            raise CredencialesInvalidasError(
                "Correo y contraseña son obligatorios."
            )

        usuario = UsuarioRepositorio.obtener_por_correo(
            correo
        )

        if not usuario or not check_password_hash(
            usuario.contrasena,
            contrasena
        ):

            raise CredencialesInvalidasError(
                "Credenciales inválidas."
            )

        access_token = _generar_access_token(
            usuario,
            self.secret_key,
            self.jwt_exp_minutes
        )

        return {
            "access_token": access_token,
            "usuario": usuario.to_dict()
        }


    def listar_todos_los_usuarios(self):

        """Devuelve una lista de todos los usuarios."""

        usuarios = UsuarioRepositorio.listar_todos()

        return [
            usuario.to_dict()
            for usuario in usuarios
        ]


    def promover_a_admin(self, correo):

        """Promueve un usuario al rol de administrador."""

        usuario = UsuarioRepositorio.obtener_por_correo(
            correo
        )

        if not usuario:

            raise UsuarioNoEncontradoError(
                f"No se encontró ningún usuario con correo {correo}."
            )

        usuario.rol = "admin"

        UsuarioRepositorio.actualizar_usuario()

        return usuario