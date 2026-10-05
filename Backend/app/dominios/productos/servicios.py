from app.dominios.productos.modelos import Producto

from app.dominios.productos.repositorios import ProductoRepositorio


class ProductoNoEncontradoError(Exception):

    pass


class ProductoServicio:

    def crear_producto(self, datos):

        producto = Producto(
            nombre=datos["nombre"],
            descripcion=datos["descripcion"],
            precio=datos["precio"],
            stock=datos["stock"],
            disponible=datos.get("disponible", True),
            categoria=datos["categoria"],
            min_fotos=datos.get("min_fotos", 1),
            max_fotos=datos.get("max_fotos", 1),
            permite_grabado=datos.get(
                "permite_grabado",
                False
            ),
            max_caracteres_grabado=datos.get(
                "max_caracteres_grabado"
            ),
            precio_grabado=datos.get(
                "precio_grabado",
                0
            ),
            permite_tarjeta=datos.get(
                "permite_tarjeta",
                False
            ),
            max_caracteres_tarjeta=datos.get(
                "max_caracteres_tarjeta"
            )
        )

        ProductoRepositorio.crear(producto)

        return producto


    def obtener_producto(self, producto_id):

        producto = ProductoRepositorio.obtener_por_id(
            producto_id
        )

        if not producto:

            raise ProductoNoEncontradoError(
                "Producto no encontrado."
            )

        return producto


    def listar_productos(self):

        productos = ProductoRepositorio.listar_todos()

        return [
            producto.to_dict()
            for producto in productos
        ]


    def actualizar_producto(
        self,
        producto_id,
        datos
    ):

        producto = ProductoRepositorio.obtener_por_id(
            producto_id
        )

        if not producto:

            raise ProductoNoEncontradoError(
                "Producto no encontrado."
            )

        producto.nombre = datos["nombre"]
        producto.descripcion = datos["descripcion"]
        producto.precio = datos["precio"]
        producto.stock = datos["stock"]
        producto.disponible = datos["disponible"]
        producto.categoria = datos["categoria"]
        producto.min_fotos = datos["min_fotos"]
        producto.max_fotos = datos["max_fotos"]

        producto.permite_grabado = datos[
            "permite_grabado"
        ]

        producto.max_caracteres_grabado = datos.get(
            "max_caracteres_grabado"
        )

        producto.precio_grabado = datos.get(
            "precio_grabado",
            0
        )

        producto.permite_tarjeta = datos[
            "permite_tarjeta"
        ]

        producto.max_caracteres_tarjeta = datos.get(
            "max_caracteres_tarjeta"
        )

        ProductoRepositorio.actualizar_producto()

        return producto


    def eliminar_producto(self, producto_id):

        producto = ProductoRepositorio.obtener_por_id(
            producto_id
        )

        if not producto:

            raise ProductoNoEncontradoError(
                "Producto no encontrado."
            )

        ProductoRepositorio.eliminar(producto)

        return True