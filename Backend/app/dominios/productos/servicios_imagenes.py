import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename

from app.dominios.productos.modelos import Producto, ImagenProducto
from app.dominios.productos.repositorios_imagenes import ImagenProductoRepositorio


class ImagenProductoNoEncontradaError(Exception):
    pass


class ImagenProductoServicio:
    EXTENSIONES_PERMITIDAS = {"jpg", "jpeg", "png", "webp"}

    def agregar_imagen(self, producto_id, archivo):
        producto = Producto.query.get(producto_id)

        if not producto:
            raise ValueError("El producto no existe.")

        if not archivo:
            raise ValueError("No se recibió ninguna imagen.")

        if not archivo.filename:
            raise ValueError("La imagen no tiene un nombre válido.")

        nombre_original = secure_filename(archivo.filename)

        extension = (
            nombre_original.rsplit(".", 1)[-1].lower()
            if "." in nombre_original
            else ""
        )

        if extension not in self.EXTENSIONES_PERMITIDAS:
            raise ValueError(
                "Formato de imagen no permitido. "
                "Use JPG, JPEG, PNG o WEBP."
            )

        # Las imágenes del catálogo no tienen límite.
        # Solo consultamos las existentes para calcular el orden.
        imagenes_existentes = (
            ImagenProductoRepositorio.listar_por_producto(producto_id)
        )

        nombre_archivo = f"{uuid.uuid4().hex}.{extension}"

        carpeta_productos = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            "productos"
        )

        os.makedirs(carpeta_productos, exist_ok=True)

        ruta_archivo = os.path.join(
            carpeta_productos,
            nombre_archivo
        )

        archivo.save(ruta_archivo)

        orden = len(imagenes_existentes) + 1

        imagen = ImagenProducto(
            producto_id=producto.id,
            url_imagen=f"/uploads/productos/{nombre_archivo}",
            orden=orden
        )

        try:
            ImagenProductoRepositorio.crear(imagen)

        except Exception:
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)

            raise

        return imagen

    def listar_imagenes(self, producto_id):
        producto = Producto.query.get(producto_id)

        if not producto:
            raise ValueError("El producto no existe.")

        return ImagenProductoRepositorio.listar_por_producto(producto_id)

    def eliminar_imagen(self, imagen_id):
        imagen = ImagenProductoRepositorio.obtener_por_id(imagen_id)

        if not imagen:
            raise ImagenProductoNoEncontradaError(
                "Imagen no encontrada."
            )

        nombre_archivo = os.path.basename(
            imagen.url_imagen
        )

        ruta_archivo = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            "productos",
            nombre_archivo
        )

        ImagenProductoRepositorio.eliminar(imagen)

        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)

        return True