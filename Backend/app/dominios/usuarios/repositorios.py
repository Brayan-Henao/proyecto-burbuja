from app.extensions import db

from app.dominios.usuarios.modelos import (
    Usuario
)




class UsuarioRepositorio:

    @staticmethod
    def obtener_por_correo(correo):
        return Usuario.query.filter_by(correo=correo).first()

    @staticmethod
    def obtener_por_id(usuario_id):
        return Usuario.query.get(usuario_id)

    @staticmethod
    def crear(usuario):
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def listar_todos():
        return Usuario.query.all()

    @staticmethod
    def actualizar_usuario():
        db.session.commit()