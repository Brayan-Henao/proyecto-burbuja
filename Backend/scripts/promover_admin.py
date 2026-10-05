from app import crear_app

from app.extensiones import db

from app.dominios.usuarios.modelos import (
    Usuario
)


app = crear_app()


with app.app_context():

    usuario = Usuario.query.filter_by(
        correo="burbujaregalosp@gmail.com"
    ).first()

    if usuario:

        usuario.rol = "admin"

        db.session.commit()

        print(
            "Usuario promovido a admin"
        )

    else:

        print(
            "Usuario no encontrado"
        )