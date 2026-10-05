from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.seguridad import token_requerido

from app.dominios.ordenes.dtos import (
    CrearOrdenDTO
)

from app.dominios.ordenes.servicios import (
    OrdenServicio,
    OrdenNoEncontradaError
)


ordenes_bp = Blueprint(
    "ordenes",
    __name__
)


orden_servicio = OrdenServicio()


@ordenes_bp.route(
    "",
    methods=["POST"]
)
@token_requerido
def crear_orden(usuario_id):

    datos = request.get_json(silent=True) or {}

    dto = CrearOrdenDTO()

    try:

        datos_validados = dto.load(
            datos
        )

    except ValidationError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": "Datos de entrada inválidos.",
                "details": err.messages
            }
        }), 400

    try:

        orden = orden_servicio.crear_orden(
            usuario_id,
            datos_validados
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
        "message": "Orden creada con éxito.",
        "data": {
            "id": orden.id,
            "usuario_id": orden.usuario_id,
            "estado": orden.estado,
            "subtotal": str(orden.subtotal),
            "envio_minimo": str(
                orden.envio_minimo
            ),
            "envio_maximo": str(
                orden.envio_maximo
            ),
            "fecha_creacion": (
                orden.fecha_creacion.isoformat()
                if orden.fecha_creacion
                else None
            )
        }
    }), 201


@ordenes_bp.route(
    "/<int:orden_id>",
    methods=["GET"]
)
@token_requerido
def obtener_orden(
    orden_id,
    usuario_id
):

    try:

        orden = orden_servicio.obtener_orden(
            orden_id
        )

    except OrdenNoEncontradaError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    if orden.usuario_id != usuario_id:

        return jsonify({
            "success": False,
            "error": {
                "message": "No tienes permiso para consultar esta orden."
            }
        }), 403

    return jsonify({
        "success": True,
        "message": "Orden encontrada.",
        "data": {
            "id": orden.id,
            "usuario_id": orden.usuario_id,
            "estado": orden.estado,
            "subtotal": str(
                orden.subtotal
            ),
            "envio_minimo": str(
                orden.envio_minimo
            ),
            "envio_maximo": str(
                orden.envio_maximo
            ),
            "fecha_creacion": (
                orden.fecha_creacion.isoformat()
                if orden.fecha_creacion
                else None
            ),
            "items": [
                {
                    "id": item.id,
                    "producto_id": item.producto_id,
                    "personalizacion_id": (
                        item.personalizacion_id
                    ),
                    "cantidad": item.cantidad,
                    "precio_unitario": str(
                        item.precio_unitario
                    ),
                    "precio_grabado": str(
                        item.precio_grabado
                    ),
                    "subtotal": str(
                        item.subtotal
                    )
                }
                for item in orden.items
            ]
        }
    }), 200


@ordenes_bp.route(
    "/usuario",
    methods=["GET"]
)
@token_requerido
def listar_ordenes_usuario(
    usuario_id
):

    ordenes = (
        orden_servicio.listar_ordenes_usuario(
            usuario_id
        )
    )

    return jsonify({
        "success": True,
        "message": "Órdenes encontradas.",
        "data": [
            {
                "id": orden.id,
                "usuario_id": orden.usuario_id,
                "estado": orden.estado,
                "subtotal": str(
                    orden.subtotal
                ),
                "envio_minimo": str(
                    orden.envio_minimo
                ),
                "envio_maximo": str(
                    orden.envio_maximo
                ),
                "fecha_creacion": (
                    orden.fecha_creacion.isoformat()
                    if orden.fecha_creacion
                    else None
                )
            }
            for orden in ordenes
        ]
    }), 200


@ordenes_bp.route(
    "/<int:orden_id>",
    methods=["DELETE"]
)
@token_requerido
def eliminar_orden(
    orden_id,
    usuario_id
):

    try:

        orden = orden_servicio.obtener_orden(
            orden_id
        )

    except OrdenNoEncontradaError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    if orden.usuario_id != usuario_id:

        return jsonify({
            "success": False,
            "error": {
                "message": "No tienes permiso para eliminar esta orden."
            }
        }), 403

    try:

        orden_servicio.eliminar_orden(
            orden_id
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
        "message": "Orden eliminada con éxito."
    }), 200