import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename

from app.dominios.personalizaciones.modelos import (
    Personalizacion,
    FotoPersonalizacion
)

from app.dominios.personalizaciones.repositorios import (
    FotoPersonalizacionRepositorio
)


class FotoPersonalizacionNoEncontradaError(Exception):

    pass


class FotoPersonalizacionServicio:

    EXTENSIONES_PERMITIDAS = {
        "jpg",
        "jpeg",
        "png",
        "webp"
    }

    def agregar_foto(
        self,
        personalizacion_id,
        archivo
    ):

        personalizacion = Personalizacion.query.get(
            personalizacion_id
        )

        if not personalizacion:

            raise ValueError(
                "La personalización no existe."
            )

        if not archivo:

            raise ValueError(
                "No se recibió ninguna imagen."
            )

        if not archivo.filename:

            raise ValueError(
                "La imagen no tiene un nombre válido."
            )

        nombre_original = secure_filename(
            archivo.filename
        )

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

        producto = personalizacion.producto_id

        cantidad_fotos = len(
            personalizacion.fotos
        )

        from app.dominios.productos.modelos import Producto

        producto_obj = Producto.query.get(
            producto
        )

        if not producto_obj:

            raise ValueError(
                "El producto de la personalización "
                "no existe."
            )

        if cantidad_fotos >= producto_obj.max_fotos:

            raise ValueError(
                "Se alcanzó el número máximo de fotos "
                "permitido para este producto."
            )

        nombre_archivo = (
            f"{uuid.uuid4().hex}.{extension}"
        )

        carpeta_personalizaciones = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            "personalizaciones"
        )

        os.makedirs(
            carpeta_personalizaciones,
            exist_ok=True
        )

        ruta_archivo = os.path.join(
            carpeta_personalizaciones,
            nombre_archivo
        )

        archivo.save(
            ruta_archivo
        )

        orden = cantidad_fotos + 1

        foto = FotoPersonalizacion(
            personalizacion_id=personalizacion.id,
            url_imagen=(
                f"/uploads/personalizaciones/"
                f"{nombre_archivo}"
            ),
            orden=orden
        )

        try:

            FotoPersonalizacionRepositorio.crear(
                foto
            )

        except Exception:

            if os.path.exists(ruta_archivo):

                os.remove(ruta_archivo)

            raise

        return foto


    def eliminar_foto(
        self,
        foto_id
    ):

        foto = FotoPersonalizacion.query.get(
            foto_id
        )

        if not foto:

            raise FotoPersonalizacionNoEncontradaError(
                "Foto de personalización no encontrada."
            )

        nombre_archivo = os.path.basename(
            foto.url_imagen
        )

        ruta_archivo = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            "personalizaciones",
            nombre_archivo
        )

        FotoPersonalizacionRepositorio.eliminar(
            foto
        )

        if os.path.exists(ruta_archivo):

            os.remove(ruta_archivo)

        return True