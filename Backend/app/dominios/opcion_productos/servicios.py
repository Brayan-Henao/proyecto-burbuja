from app.dominios.opcion_productos.modelos import OpcionProducto
from app.dominios.opcion_productos.repositorios import OpcionProductoRepositorio


class OpcionProductoNoEncontradaError(Exception):
    pass


class OpcionProductoServicio:

    def _validar_opcion_principal(
        self,
        producto_id,
        opcion_principal_id,
        opcion_id=None
    ):
        if opcion_principal_id is None:
            return

        opcion_principal = (
            OpcionProductoRepositorio.obtener_por_id(
                opcion_principal_id
            )
        )

        if not opcion_principal:
            raise OpcionProductoNoEncontradaError(
                "La opción principal no existe."
            )

        if opcion_principal.producto_id != producto_id:
            raise ValueError(
                "La opción principal debe pertenecer "
                "al mismo producto."
            )

        if opcion_id is not None:
            if opcion_principal_id == opcion_id:
                raise ValueError(
                    "Una opción no puede ser "
                    "su propia opción principal."
                )

            opcion_actual = opcion_principal

            while opcion_actual.opcion_principal_id is not None:

                if opcion_actual.opcion_principal_id == opcion_id:
                    raise ValueError(
                        "No se puede crear una relación "
                        "circular entre las opciones."
                    )

                opcion_actual = (
                    OpcionProductoRepositorio.obtener_por_id(
                        opcion_actual.opcion_principal_id
                    )
                )

                if not opcion_actual:
                    break

    def crear_opcion(self, datos):

        opcion_principal_id = datos.get(
            "opcion_principal_id"
        )

        self._validar_opcion_principal(
            datos["producto_id"],
            opcion_principal_id
        )

        opcion = OpcionProducto(
            producto_id=datos["producto_id"],
            tipo=datos["tipo"],
            valor=datos["valor"],
            activa=datos.get("activa", True),
            opcion_principal_id=opcion_principal_id
        )

        OpcionProductoRepositorio.crear(opcion)

        return opcion

    def obtener_opcion(self, opcion_id):

        opcion = OpcionProductoRepositorio.obtener_por_id(
            opcion_id
        )

        if not opcion:
            raise OpcionProductoNoEncontradaError(
                "Opción de producto no encontrada."
            )

        return opcion

    def listar_opciones_por_producto(self, producto_id):

        opciones = OpcionProductoRepositorio.listar_por_producto(
            producto_id
        )

        return opciones

    def actualizar_opcion(self, opcion_id, datos):

        opcion = OpcionProductoRepositorio.obtener_por_id(
            opcion_id
        )

        if not opcion:
            raise OpcionProductoNoEncontradaError(
                "Opción de producto no encontrada."
            )

        opcion_principal_id = datos.get(
            "opcion_principal_id"
        )

        self._validar_opcion_principal(
            opcion.producto_id,
            opcion_principal_id,
            opcion_id
        )

        opcion.tipo = datos["tipo"]
        opcion.valor = datos["valor"]
        opcion.activa = datos["activa"]
        opcion.opcion_principal_id = opcion_principal_id

        OpcionProductoRepositorio.actualizar()

        return opcion

    def eliminar_opcion(self, opcion_id):

        opcion = OpcionProductoRepositorio.obtener_por_id(
            opcion_id
        )

        if not opcion:
            raise OpcionProductoNoEncontradaError(
                "Opción de producto no encontrada."
            )

        OpcionProductoRepositorio.eliminar(opcion)

        return True