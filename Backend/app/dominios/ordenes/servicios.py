from app.extensions import db

from app.dominios.ordenes.modelos import (
    Orden,
    OrdenItem
)

from app.dominios.ordenes.repositorios import (
    OrdenRepositorio,
    OrdenItemRepositorio
)

from app.dominios.productos.modelos import Producto

from app.dominios.personalizaciones.modelos import (
    Personalizacion
)


class OrdenNoEncontradaError(Exception):

    pass


class OrdenServicio:

    def crear_orden(
        self,
        usuario_id,
        datos
    ):

        items_datos = datos["items"]

        if not items_datos:

            raise ValueError(
                "La orden debe contener al menos un producto."
            )

        try:

            subtotal_orden = 0

            orden = Orden(
                usuario_id=usuario_id,
                estado="pendiente",
                subtotal=0,
                envio_minimo=0,
                envio_maximo=0
            )

            db.session.add(orden)

            for item_data in items_datos:

                producto = Producto.query.get(
                    item_data["producto_id"]
                )

                if not producto:

                    raise ValueError(
                        "El producto de la orden no existe."
                    )

                if not producto.disponible:

                    raise ValueError(
                        "El producto no está disponible."
                    )

                cantidad = item_data.get(
                    "cantidad",
                    1
                )

                if cantidad <= 0:

                    raise ValueError(
                        "La cantidad debe ser mayor que cero."
                    )

                if producto.stock < cantidad:

                    raise ValueError(
                        "No hay suficiente stock para el producto."
                    )

                personalizacion_id = item_data.get(
                    "personalizacion_id"
                )

                personalizacion = None

                if personalizacion_id:

                    personalizacion = (
                        Personalizacion.query.get(
                            personalizacion_id
                        )
                    )

                    if not personalizacion:

                        raise ValueError(
                            "La personalización de la orden no existe."
                        )

                    if (
                        personalizacion.producto_id
                        != producto.id
                    ):

                        raise ValueError(
                            "La personalización no pertenece "
                            "al producto de la orden."
                        )

                precio_unitario = producto.precio

                precio_grabado = 0

                if personalizacion:

                    if personalizacion.grabado:

                        if not producto.permite_grabado:

                            raise ValueError(
                                "El producto no permite grabado."
                            )

                        precio_grabado = (
                            producto.precio_grabado
                        )

                subtotal_item = (
                    (
                        precio_unitario
                        + precio_grabado
                    )
                    * cantidad
                )

                item = OrdenItem(
                    orden=orden,
                    producto_id=producto.id,
                    personalizacion_id=(
                        personalizacion.id
                        if personalizacion
                        else None
                    ),
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    precio_grabado=precio_grabado,
                    subtotal=subtotal_item
                )

                db.session.add(item)

                subtotal_orden += subtotal_item

            orden.subtotal = subtotal_orden

            db.session.commit()

            return orden

        except Exception:

            db.session.rollback()

            raise


    def obtener_orden(
        self,
        orden_id
    ):

        orden = OrdenRepositorio.obtener_por_id(
            orden_id
        )

        if not orden:

            raise OrdenNoEncontradaError(
                "Orden no encontrada."
            )

        return orden


    def listar_ordenes_usuario(
        self,
        usuario_id
    ):

        return OrdenRepositorio.listar_por_usuario(
            usuario_id
        )


    def eliminar_orden(
        self,
        orden_id
    ):

        orden = self.obtener_orden(
            orden_id
        )

        if orden.estado != "pendiente":

            raise ValueError(
                "Solo se pueden eliminar órdenes pendientes."
            )

        OrdenRepositorio.eliminar(
            orden
        )

        return True