from flask import Blueprint, request, jsonify

from marshmallow import ValidationError

from app.seguridad import token_requerido

from app.dominios.pagos.dtos import (
    CrearPagoDTO
)

from app.dominios.pagos.servicios import (
    PagoServicio,
    PagoNoEncontradoError
)


pagos_bp = Blueprint(
    "pagos",
    __name__
)


pago_servicio = PagoServicio()


@pagos_bp.route(
    "",
    methods=["POST"]
)
@token_requerido
def crear_pago(
    usuario_id
):

    datos = request.get_json(
        silent=True
    ) or {}

    dto = CrearPagoDTO()

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

        pago = pago_servicio.crear_pago(
            usuario_id,
            datos_validados["orden_id"]
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
        "message": "Pago creado con éxito.",
        "data": pago.to_dict()
    }), 201


@pagos_bp.route(
    "/<int:pago_id>",
    methods=["GET"]
)
@token_requerido
def obtener_pago(
    pago_id,
    usuario_id
):

    try:

        pago = pago_servicio.obtener_pago(
            pago_id
        )

    except PagoNoEncontradoError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    if pago.orden.usuario_id != usuario_id:

        return jsonify({
            "success": False,
            "error": {
                "message": "No tienes permiso para consultar este pago."
            }
        }), 403

    return jsonify({
        "success": True,
        "message": "Pago encontrado.",
        "data": pago.to_dict()
    }), 200


@pagos_bp.route(
    "/orden/<int:orden_id>",
    methods=["GET"]
)
@token_requerido
def listar_pagos_orden(
    orden_id,
    usuario_id
):

    try:

        pagos = pago_servicio.listar_pagos_orden(
            usuario_id,
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
        "message": "Pagos encontrados.",
        "data": [
            pago.to_dict()
            for pago in pagos
        ]
    }), 200


@pagos_bp.route(
    "/<int:pago_id>/checkout",
    methods=["GET"]
)
@token_requerido
def obtener_datos_checkout(
    pago_id,
    usuario_id
):

    try:

        pago = pago_servicio.obtener_pago(
            pago_id
        )

    except PagoNoEncontradoError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    if pago.orden.usuario_id != usuario_id:

        return jsonify({
            "success": False,
            "error": {
                "message": "No tienes permiso para usar este pago."
            }
        }), 403

    if pago.estado != "pendiente":

        return jsonify({
            "success": False,
            "error": {
                "message": "El pago ya no está pendiente."
            }
        }), 400

    try:

        firma = (
            pago_servicio.generar_firma_integridad(
                pago
            )
        )

        datos_checkout = {
            "public_key": (
                pago_servicio.obtener_llave_publica()
            ),
            "currency": "COP",
            "amount_in_cents": int(
                pago.monto * 100
            ),
            "reference": pago.referencia,
            "signature": firma
        }

    except ValueError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 500

    return jsonify({
        "success": True,
        "message": (
            "Datos de checkout generados correctamente."
        ),
        "data": datos_checkout
    }), 200