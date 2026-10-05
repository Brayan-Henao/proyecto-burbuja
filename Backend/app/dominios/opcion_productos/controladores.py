from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.seguridad import admin_requerido

from app.dominios.opcion_productos.dtos import (
    CrearOpcionProductoDTO,
    ActualizarOpcionProductoDTO
)

from app.dominios.opcion_productos.servicios import (
    OpcionProductoServicio,
    OpcionProductoNoEncontradaError
)


opciones_productos_bp = Blueprint(
    "opciones_productos",
    __name__
)


opcion_producto_servicio = OpcionProductoServicio()


@opciones_productos_bp.route("", methods=["POST"])
@admin_requerido
def crear_opcion(usuario_id):
    datos = request.get_json(silent=True) or {}

    dto = CrearOpcionProductoDTO()

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
        opcion = opcion_producto_servicio.crear_opcion(
            datos_validados
        )

    except OpcionProductoNoEncontradaError as err:
        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    except ValueError as err:
        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 400

    return jsonify({
        "success": True,
        "message": "Opción de producto creada con éxito.",
        "data": {
            "id": opcion.id,
            "producto_id": opcion.producto_id,
            "tipo": opcion.tipo,
            "valor": opcion.valor,
            "activa": opcion.activa,
            "opcion_principal_id": opcion.opcion_principal_id
        }
    }), 201


@opciones_productos_bp.route(
    "/<int:opcion_id>",
    methods=["GET"]
)
def obtener_opcion(opcion_id):
    try:
        opcion = opcion_producto_servicio.obtener_opcion(
            opcion_id
        )

    except OpcionProductoNoEncontradaError as err:
        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    return jsonify({
        "success": True,
        "message": "Opción de producto encontrada.",
        "data": {
            "id": opcion.id,
            "producto_id": opcion.producto_id,
            "tipo": opcion.tipo,
            "valor": opcion.valor,
            "activa": opcion.activa,
            "opcion_principal_id": opcion.opcion_principal_id
        }
    }), 200


@opciones_productos_bp.route(
    "/producto/<int:producto_id>",
    methods=["GET"]
)
def listar_opciones_por_producto(producto_id):

    opciones = opcion_producto_servicio.listar_opciones_por_producto(
        producto_id
    )

    return jsonify({
        "success": True,
        "message": "Lista de opciones del producto.",
        "data": [
            {
                "id": opcion.id,
                "producto_id": opcion.producto_id,
                "tipo": opcion.tipo,
                "valor": opcion.valor,
                "activa": opcion.activa,
                "opcion_principal_id": opcion.opcion_principal_id,
                "opciones_dependientes": [
                    {
                        "id": dependiente.id,
                        "producto_id": dependiente.producto_id,
                        "tipo": dependiente.tipo,
                        "valor": dependiente.valor,
                        "activa": dependiente.activa,
                        "opcion_principal_id": dependiente.opcion_principal_id
                    }
                    for dependiente in opcion.opciones_dependientes
                ]
            }
            for opcion in opciones
            if opcion.opcion_principal_id is None
        ]
    }), 200


@opciones_productos_bp.route(
    "/<int:opcion_id>",
    methods=["PUT"]
)
@admin_requerido
def actualizar_opcion(opcion_id, usuario_id):
    datos = request.get_json(silent=True) or {}

    dto = ActualizarOpcionProductoDTO()

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
        opcion = opcion_producto_servicio.actualizar_opcion(
            opcion_id,
            datos_validados
        )

    except OpcionProductoNoEncontradaError as err:
        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    except ValueError as err:
        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 400

    return jsonify({
        "success": True,
        "message": "Opción de producto actualizada con éxito.",
        "data": {
            "id": opcion.id,
            "producto_id": opcion.producto_id,
            "tipo": opcion.tipo,
            "valor": opcion.valor,
            "activa": opcion.activa,
            "opcion_principal_id": opcion.opcion_principal_id
        }
    }), 200


@opciones_productos_bp.route(
    "/<int:opcion_id>",
    methods=["DELETE"]
)
@admin_requerido
def eliminar_opcion(opcion_id, usuario_id):
    try:
        opcion_producto_servicio.eliminar_opcion(
            opcion_id
        )

    except OpcionProductoNoEncontradaError as err:
        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    return jsonify({
        "success": True,
        "message": "Opción de producto eliminada con éxito."
    }), 200