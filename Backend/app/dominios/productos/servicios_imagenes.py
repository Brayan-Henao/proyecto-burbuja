import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename

from app.dominios.productos.modelos import (
    Producto,
    ImagenProducto
)

from app.dominios.productos.repositorios_imagenes import (
    ImagenProductoRepositorio
)


class ImagenProductoNoEncontradaError(Exception):

    pass


class ImagenProductoServicio:

    EXTENSIONES_PERMITIDAS = {
        "jpg",
        "jpeg",
        "png",
        "webp"
    }

    def agregar_imagen(
        self,
        producto_id,
        archivo
    ):

        # 1. Verificar que el producto existe

        producto = Producto.query.get(
            producto_id
        )

        if not producto:

            raise ValueError(
                "El producto no existe."
            )


        # 2. Verificar que se recibió un archivo

        if not archivo:

            raise ValueError(
                "No se recibió ninguna imagen."
            )


        # 3. Verificar que el archivo tenga nombre

        if not archivo.filename:

            raise ValueError(
                "La imagen no tiene un nombre válido."
            )


        # 4. Obtener la extensión

        nombre_original = secure_filename(
            archivo.filename
        )

        extension = (
            nombre_original
            .rsplit(".", 1)[-1]
            .lower()
            if "." in nombre_original
            else ""
        )


        # 5. Verificar la extensión

        if extension not in self.EXTENSIONES_PERMITIDAS:

            raise ValueError(
                "Formato de imagen no permitido. "
                "Use JPG, JPEG, PNG o WEBP."
            )


        # 6. Verificar el número máximo de imágenes

        imagenes_existentes = (
            ImagenProductoRepositorio
            .listar_por_producto(
                producto_id
            )
        )

        if len(imagenes_existentes) >= producto.max_fotos:

            raise ValueError(
                "El producto ya tiene el número "
                "máximo de imágenes permitido."
            )


        # 7. Generar un nombre único

        nombre_archivo = (
            f"{uuid.uuid4().hex}.{extension}"
        )


        # 8. Obtener la carpeta de almacenamiento

        carpeta_productos = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            "productos"
        )

        os.makedirs(
            carpeta_productos,
            exist_ok=True
        )


        # 9. Crear la ruta física del archivo

        ruta_archivo = os.path.join(
            carpeta_productos,
            nombre_archivo
        )


        # 10. Guardar físicamente la imagen

        archivo.save(
            ruta_archivo
        )


        # 11. Calcular el orden de la imagen

        orden = len(
            imagenes_existentes
        ) + 1


        # 12. Crear el registro en la base de datos

        imagen = ImagenProducto(
            producto_id=producto.id,
            url_imagen=(
                f"/uploads/productos/"
                f"{nombre_archivo}"
            ),
            orden=orden
        )


        # 13. Guardar el registro

        try:

            ImagenProductoRepositorio.crear(
                imagen
            )

        except Exception:

            # Si falla la base de datos,
            # eliminamos el archivo físico.

            if os.path.exists(
                ruta_archivo
            ):

                os.remove(
                    ruta_archivo
                )

            raise


        return imagen


    def listar_imagenes(
        self,
        producto_id
    ):

        producto = Producto.query.get(
            producto_id
        )

        if not producto:

            raise ValueError(
                "El producto no existe."
            )

        return (
            ImagenProductoRepositorio
            .listar_por_producto(
                producto_id
            )
        )


    def eliminar_imagen(
        self,
        imagen_id
    ):

        imagen = (
            ImagenProductoRepositorio
            .obtener_por_id(
                imagen_id
            )
        )

        if not imagen:

            raise ImagenProductoNoEncontradaError(
                "Imagen no encontrada."
            )


        # Guardamos la ruta física antes de eliminar
        # el registro de la base de datos.

        nombre_archivo = os.path.basename(
            imagen.url_imagen
        )

        ruta_archivo = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            "productos",
            nombre_archivo
        )


        # Eliminar registro de la base de datos

        ImagenProductoRepositorio.eliminar(
            imagen
        )


        # Eliminar archivo físico

        if os.path.exists(
            ruta_archivo
        ):

            os.remove(
                ruta_archivo
            )


        return True
    