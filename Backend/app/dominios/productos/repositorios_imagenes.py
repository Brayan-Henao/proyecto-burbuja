from app.extensions import db

from app.dominios.productos.modelos import (
    ImagenProducto
)


class ImagenProductoRepositorio:

    @staticmethod
    def obtener_por_id(imagen_id):

        return ImagenProducto.query.get(
            imagen_id
        )


    @staticmethod
    def listar_por_producto(producto_id):

        return ImagenProducto.query.filter_by(
            producto_id=producto_id
        ).order_by(
            ImagenProducto.orden.asc()
        ).all()


    @staticmethod
    def crear(imagen):

        db.session.add(imagen)
        db.session.commit()

        return imagen


    @staticmethod
    def eliminar(imagen):

        db.session.delete(imagen)
        db.session.commit()