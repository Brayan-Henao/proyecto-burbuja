from app.extensions import db
from app.dominios.opcion_productos.modelos import OpcionProducto


class OpcionProductoRepositorio:

    @staticmethod
    def obtener_por_id(opcion_id):
        return OpcionProducto.query.get(opcion_id)

    @staticmethod
    def listar_por_producto(producto_id):
        return OpcionProducto.query.filter_by(
            producto_id=producto_id
        ).all()

    @staticmethod
    def crear(opcion):
        db.session.add(opcion)
        db.session.commit()
        return opcion

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def eliminar(opcion):
        db.session.delete(opcion)
        db.session.commit()