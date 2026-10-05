from app.extensions import db

from app.dominios.personalizaciones.modelos import (
    Personalizacion,
    FotoPersonalizacion,
    OpcionPersonalizacion
)


class PersonalizacionRepositorio:

    @staticmethod
    def obtener_por_id(personalizacion_id):
        return Personalizacion.query.get(
            personalizacion_id
        )

    @staticmethod
    def crear(personalizacion):
        db.session.add(personalizacion)
        db.session.commit()

        return personalizacion

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def eliminar(personalizacion):
        db.session.delete(personalizacion)
        db.session.commit()


class FotoPersonalizacionRepositorio:

    @staticmethod
    def crear(foto):
        db.session.add(foto)
        db.session.commit()

        return foto

    @staticmethod
    def eliminar(foto):
        db.session.delete(foto)
        db.session.commit()


class OpcionPersonalizacionRepositorio:

    @staticmethod
    def crear(opcion):
        db.session.add(opcion)
        db.session.commit()

        return opcion

    @staticmethod
    def eliminar(opcion):
        db.session.delete(opcion)
        db.session.commit()