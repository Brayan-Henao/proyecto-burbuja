from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.seguridad import token_requerido

from app.dominios.personalizaciones.dtos import (
    CrearPersonalizacionDTO,
    ActualizarPersonalizacionDTO,
    AgregarOpcionPersonalizacionDTO
)

from app.dominios.personalizaciones.servicios import (
    PersonalizacionServicio,
    PersonalizacionNoEncontradaError
)

from app.dominios.personalizaciones.servicios_fotos import (
    FotoPersonalizacionServicio,
    FotoPersonalizacionNoEncontradaError
)


personalizaciones_bp = Blueprint(
    "personalizaciones",
    __name__
)


personalizacion_servicio = PersonalizacionServicio()

foto_personalizacion_servicio = (
    FotoPersonalizacionServicio()
)


@personalizaciones_bp.route(
    "",
    methods=["POST"]
)
@token_requerido
def crear_personalizacion(usuario_id):

    datos = request.get_json(silent=True) or {}

    dto = CrearPersonalizacionDTO()

    try:

        datos_validados = dto.load(datos)

    except ValidationError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": "Datos de entrada inválidos.",
                "details": err.messages
            }
        }), 400

    try:

        personalizacion = (
            personalizacion_servicio.crear_personalizacion(
                usuario_id,
                datos_validados
            )
        )

    except ValueError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 400

    return jsonify({
        "success": True,
        "message": "Personalización creada con éxito.",
        "data": {
            "id": personalizacion.id,
            "usuario_id": personalizacion.usuario_id,
            "producto_id": personalizacion.producto_id,
            "grabado": personalizacion.grabado,
            "mensaje": personalizacion.mensaje,
            "fecha_creacion": (
                personalizacion.fecha_creacion.isoformat()
                if personalizacion.fecha_creacion
                else None
            )
        }
    }), 201


@personalizaciones_bp.route(
    "/<int:personalizacion_id>",
    methods=["GET"]
)
@token_requerido
def obtener_personalizacion(
    personalizacion_id,
    usuario_id
):

    try:

        personalizacion = (
            personalizacion_servicio.obtener_personalizacion(
                usuario_id,
                personalizacion_id
            )
        )

    except PersonalizacionNoEncontradaError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    except PermissionError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 403

    return jsonify({
        "success": True,
        "message": "Personalización encontrada.",
        "data": {
            "id": personalizacion.id,
            "usuario_id": personalizacion.usuario_id,
            "producto_id": personalizacion.producto_id,
            "grabado": personalizacion.grabado,
            "mensaje": personalizacion.mensaje,
            "fecha_creacion": (
                personalizacion.fecha_creacion.isoformat()
                if personalizacion.fecha_creacion
                else None
            ),
            "fotos": [
                {
                    "id": foto.id,
                    "url_imagen": foto.url_imagen,
                    "orden": foto.orden
                }
                for foto in personalizacion.fotos
            ],
            "opciones": [
                {
                    "id": opcion.id,
                    "opcion_producto_id": (
                        opcion.opcion_producto_id
                    )
                }
                for opcion in personalizacion.opciones
            ]
        }
    }), 200


@personalizaciones_bp.route(
    "/<int:personalizacion_id>",
    methods=["PUT"]
)
@token_requerido
def actualizar_personalizacion(
    personalizacion_id,
    usuario_id
):

    datos = request.get_json(silent=True) or {}

    dto = ActualizarPersonalizacionDTO()

    try:

        datos_validados = dto.load(datos)

    except ValidationError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": "Datos de entrada inválidos.",
                "details": err.messages
            }
        }), 400

    try:

        personalizacion = (
            personalizacion_servicio.actualizar_personalizacion(
                usuario_id,
                personalizacion_id,
                datos_validados
            )
        )

    except PersonalizacionNoEncontradaError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    except PermissionError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 403

    except ValueError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 400

    return jsonify({
        "success": True,
        "message": "Personalización actualizada con éxito.",
        "data": {
            "id": personalizacion.id,
            "usuario_id": personalizacion.usuario_id,
            "producto_id": personalizacion.producto_id,
            "grabado": personalizacion.grabado,
            "mensaje": personalizacion.mensaje
        }
    }), 200


@personalizaciones_bp.route(
    "/<int:personalizacion_id>",
    methods=["DELETE"]
)
@token_requerido
def eliminar_personalizacion(
    personalizacion_id,
    usuario_id
):

    try:

        personalizacion_servicio.eliminar_personalizacion(
            usuario_id,
            personalizacion_id
        )

    except PersonalizacionNoEncontradaError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    except PermissionError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 403

    return jsonify({
        "success": True,
        "message": "Personalización eliminada con éxito."
    }), 200


@personalizaciones_bp.route(
    "/<int:personalizacion_id>/fotos",
    methods=["POST"]
)
@token_requerido
def agregar_foto(
    personalizacion_id,
    usuario_id
):

    archivo = request.files.get(
        "imagen"
    )

    try:

        foto = (
            foto_personalizacion_servicio.agregar_foto(
                usuario_id,
                personalizacion_id,
                archivo
            )
        )

    except ValueError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 400

    except PermissionError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 403

    return jsonify({
        "success": True,
        "message": (
            "Foto agregada a la personalización."
        ),
        "data": {
            "id": foto.id,
            "personalizacion_id": (
                foto.personalizacion_id
            ),
            "url_imagen": foto.url_imagen,
            "orden": foto.orden
        }
    }), 201


@personalizaciones_bp.route(
    "/fotos/<int:foto_id>",
    methods=["DELETE"]
)
@token_requerido
def eliminar_foto(
    foto_id,
    usuario_id
):

    try:

        foto_personalizacion_servicio.eliminar_foto(
            usuario_id,
            foto_id
        )

    except FotoPersonalizacionNoEncontradaError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    except PermissionError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 403

    return jsonify({
        "success": True,
        "message": (
            "Foto de personalización eliminada "
            "con éxito."
        )
    }), 200


@personalizaciones_bp.route(
    "/<int:personalizacion_id>/opciones",
    methods=["POST"]
)
@token_requerido
def agregar_opcion(
    personalizacion_id,
    usuario_id
):

    datos = request.get_json(silent=True) or {}

    dto = AgregarOpcionPersonalizacionDTO()

    try:

        datos_validados = dto.load(datos)

    except ValidationError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": "Datos de entrada inválidos.",
                "details": err.messages
            }
        }), 400

    try:

        opcion = personalizacion_servicio.agregar_opcion(
            usuario_id,
            personalizacion_id,
            datos_validados
        )

    except PersonalizacionNoEncontradaError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    except PermissionError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 403

    except ValueError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 400

    return jsonify({
        "success": True,
        "message": (
            "Opción agregada a la personalización."
        ),
        "data": {
            "id": opcion.id,
            "personalizacion_id": (
                opcion.personalizacion_id
            ),
            "opcion_producto_id": (
                opcion.opcion_producto_id
            )
        }
    }), 201