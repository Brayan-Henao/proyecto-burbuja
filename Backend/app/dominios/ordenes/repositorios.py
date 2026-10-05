from app.extensions import db

from app.dominios.ordenes.modelos import (
    Orden,
    OrdenItem
)


class OrdenRepositorio:

    @staticmethod
    def obtener_por_id(orden_id):

        return Orden.query.get(orden_id)


    @staticmethod
    def listar_por_usuario(usuario_id):

        return Orden.query.filter_by(
            usuario_id=usuario_id
        ).all()


    @staticmethod
    def crear(orden):

        db.session.add(orden)
        db.session.commit()

        return orden


    @staticmethod
    def actualizar():

        db.session.commit()


    @staticmethod
    def eliminar(orden):

        db.session.delete(orden)
        db.session.commit()


class OrdenItemRepositorio:

    @staticmethod
    def obtener_por_id(item_id):

        return OrdenItem.query.get(item_id)


    @staticmethod
    def listar_por_orden(orden_id):

        return OrdenItem.query.filter_by(
            orden_id=orden_id
        ).all()


    @staticmethod
    def crear(item):

        db.session.add(item)
        db.session.commit()

        return item


    @staticmethod
    def eliminar(item):

        db.session.delete(item)
        db.session.commit()