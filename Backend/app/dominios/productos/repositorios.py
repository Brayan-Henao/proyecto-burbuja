from app.extensions import db

from app.dominios.productos.modelos import Producto


class ProductoRepositorio:

    @staticmethod
    def obtener_por_id(producto_id):
        return Producto.query.get(producto_id)

    @staticmethod
    def crear(producto):
        db.session.add(producto)
        db.session.commit()
        return producto

    @staticmethod
    def listar_todos():
        return Producto.query.all()

    @staticmethod
    def actualizar_producto():
        db.session.commit()

    @staticmethod
    def eliminar(producto):
        db.session.delete(producto)
        db.session.commit()