from app.dominios.personalizaciones.modelos import (
    Personalizacion,
    FotoPersonalizacion,
    OpcionPersonalizacion
)

from app.dominios.personalizaciones.repositorios import (
    PersonalizacionRepositorio,
    FotoPersonalizacionRepositorio,
    OpcionPersonalizacionRepositorio
)

from app.dominios.opcion_productos.modelos import (
    OpcionProducto
)

from app.dominios.productos.modelos import (
    Producto
)


class PersonalizacionNoEncontradaError(Exception):
    pass


class PersonalizacionServicio:

    def crear_personalizacion(
        self,
        usuario_id,
        datos
    ):

        producto = Producto.query.get(
            datos["producto_id"]
        )

        if not producto:

            raise ValueError(
                "El producto de la personalización no existe."
            )

        if "grabado" in datos:

            grabado = datos.get("grabado")

            if grabado:

                if not producto.permite_grabado:

                    raise ValueError(
                        "Este producto no permite grabado."
                    )

                if (
                    producto.max_caracteres_grabado
                    and len(grabado)
                    > producto.max_caracteres_grabado
                ):

                    raise ValueError(
                        "El grabado supera el número máximo "
                        "de caracteres permitido."
                    )

        if "mensaje" in datos:

            mensaje = datos.get("mensaje")

            if mensaje:

                if not producto.permite_tarjeta:

                    raise ValueError(
                        "Este producto no permite tarjeta."
                    )

                if (
                    producto.max_caracteres_tarjeta
                    and len(mensaje)
                    > producto.max_caracteres_tarjeta
                ):

                    raise ValueError(
                        "El mensaje supera el número máximo "
                        "de caracteres permitido para la tarjeta."
                    )

        personalizacion = Personalizacion(
            usuario_id=usuario_id,
            producto_id=datos["producto_id"],
            grabado=datos.get("grabado"),
            mensaje=datos.get("mensaje")
        )

        PersonalizacionRepositorio.crear(
            personalizacion
        )

        return personalizacion


    def obtener_personalizacion(
        self,
        usuario_id,
        personalizacion_id
    ):

        personalizacion = (
            PersonalizacionRepositorio.obtener_por_id(
                personalizacion_id
            )
        )

        if not personalizacion:

            raise PersonalizacionNoEncontradaError(
                "Personalización no encontrada."
            )

        if personalizacion.usuario_id != usuario_id:

            raise PermissionError(
                "No tienes permiso para acceder a esta personalización."
            )

        return personalizacion


    def actualizar_personalizacion(
        self,
        usuario_id,
        personalizacion_id,
        datos
    ):

        personalizacion = self.obtener_personalizacion(
            usuario_id,
            personalizacion_id
        )

        producto = Producto.query.get(
            personalizacion.producto_id
        )

        if not producto:

            raise ValueError(
                "El producto de la personalización no existe."
            )

        if "grabado" in datos:

            grabado = datos.get("grabado")

            if grabado:

                if not producto.permite_grabado:

                    raise ValueError(
                        "Este producto no permite grabado."
                    )

                if (
                    producto.max_caracteres_grabado
                    and len(grabado)
                    > producto.max_caracteres_grabado
                ):

                    raise ValueError(
                        "El grabado supera el número máximo "
                        "de caracteres permitido."
                    )

            personalizacion.grabado = grabado

        if "mensaje" in datos:

            mensaje = datos.get("mensaje")

            if mensaje:

                if not producto.permite_tarjeta:

                    raise ValueError(
                        "Este producto no permite tarjeta."
                    )

                if (
                    producto.max_caracteres_tarjeta
                    and len(mensaje)
                    > producto.max_caracteres_tarjeta
                ):

                    raise ValueError(
                        "El mensaje supera el número máximo "
                        "de caracteres permitido para la tarjeta."
                    )

            personalizacion.mensaje = mensaje

        PersonalizacionRepositorio.actualizar()

        return personalizacion


    def eliminar_personalizacion(
        self,
        usuario_id,
        personalizacion_id
    ):

        personalizacion = self.obtener_personalizacion(
            usuario_id,
            personalizacion_id
        )

        PersonalizacionRepositorio.eliminar(
            personalizacion
        )

        return True


    def agregar_foto(
        self,
        usuario_id,
        personalizacion_id,
        datos
    ):

        personalizacion = self.obtener_personalizacion(
            usuario_id,
            personalizacion_id
        )

        producto = Producto.query.get(
            personalizacion.producto_id
        )

        if not producto:

            raise ValueError(
                "El producto de la personalización no existe."
            )

        cantidad_fotos = len(
            personalizacion.fotos
        )

        if cantidad_fotos >= producto.max_fotos:

            raise ValueError(
                "Se alcanzó el número máximo "
                "de fotos permitido para este producto."
            )

        foto = FotoPersonalizacion(
            personalizacion_id=personalizacion.id,
            url_imagen=datos["url_imagen"],
            orden=datos.get("orden", 1)
        )

        FotoPersonalizacionRepositorio.crear(
            foto
        )

        return foto


    def agregar_opcion(
        self,
        usuario_id,
        personalizacion_id,
        datos
    ):

        personalizacion = self.obtener_personalizacion(
            usuario_id,
            personalizacion_id
        )

        opcion = OpcionProducto.query.get(
            datos["opcion_producto_id"]
        )

        if not opcion:

            raise ValueError(
                "La opción de producto no existe."
            )

        if opcion.producto_id != personalizacion.producto_id:

            raise ValueError(
                "La opción de producto no pertenece "
                "al mismo producto de la personalización."
            )

        if not opcion.activa:

            raise ValueError(
                "La opción de producto no está disponible."
            )

        opcion_personalizacion = OpcionPersonalizacion(
            personalizacion_id=personalizacion.id,
            opcion_producto_id=opcion.id
        )

        OpcionPersonalizacionRepositorio.crear(
            opcion_personalizacion
        )

        return opcion_personalizacion