from flask import Blueprint, request, jsonify

from marshmallow import ValidationError

from app.dominios.productos.dtos import (
    CrearProductoDTO,
    ActualizarProductoDTO
)

from app.dominios.productos.servicios import (
    ProductoNoEncontradoError
)

from app.dominios.productos.servicios_imagenes import (
    ImagenProductoServicio,
    ImagenProductoNoEncontradaError
)

from app.seguridad import admin_requerido


productos_bp = Blueprint(
    "productos",
    __name__
)

admin_productos_bp = Blueprint(
    "admin_productos",
    __name__
)


producto_servicio = None

imagen_producto_servicio = ImagenProductoServicio()


# ==========================================
# RUTAS DE PRODUCTOS
# ==========================================

@productos_bp.route("", methods=["GET"])
def listar_productos():

    lista = producto_servicio.listar_productos()

    return jsonify({
        "success": True,
        "message": "Lista de productos.",
        "data": lista
    }), 200


@productos_bp.route(
    "/<int:producto_id>",
    methods=["GET"]
)
def obtener_producto(producto_id):

    try:

        producto = producto_servicio.obtener_producto(
            producto_id
        )

    except ProductoNoEncontradoError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    return jsonify({
        "success": True,
        "message": "Producto encontrado.",
        "data": producto.to_dict()
    }), 200


# ==========================================
# RUTAS DE ADMINISTRACIÓN
# ==========================================

@admin_productos_bp.route(
    "/productos",
    methods=["POST"]
)
@admin_requerido
def crear_producto(usuario_id):

    datos = request.get_json(
        silent=True
    ) or {}

    dto = CrearProductoDTO()

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

    producto = producto_servicio.crear_producto(
        datos_validados
    )

    return jsonify({
        "success": True,
        "message": "Producto creado con éxito.",
        "data": {
            "id": producto.id,
            "nombre": producto.nombre
        }
    }), 201


@admin_productos_bp.route(
    "/productos/<int:producto_id>",
    methods=["PUT"]
)
@admin_requerido
def actualizar_producto(
    usuario_id,
    producto_id
):

    datos = request.get_json(
        silent=True
    ) or {}

    dto = ActualizarProductoDTO()

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

        producto = producto_servicio.actualizar_producto(
            producto_id,
            datos_validados
        )

    except ProductoNoEncontradoError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    return jsonify({
        "success": True,
        "message": "Producto actualizado con éxito.",
        "data": {
            "id": producto.id,
            "nombre": producto.nombre
        }
    }), 200


@admin_productos_bp.route(
    "/productos/<int:producto_id>",
    methods=["DELETE"]
)
@admin_requerido
def eliminar_producto(
    usuario_id,
    producto_id
):

    try:

        producto_servicio.eliminar_producto(
            producto_id
        )

    except ProductoNoEncontradoError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    return jsonify({
        "success": True,
        "message": "Producto eliminado con éxito."
    }), 200


# ==========================================
# IMÁGENES DE PRODUCTOS
# ==========================================

@admin_productos_bp.route(
    "/productos/<int:producto_id>/imagenes",
    methods=["POST"]
)
@admin_requerido
def agregar_imagen_producto(
    usuario_id,
    producto_id
):

    archivo = request.files.get(
        "imagen"
    )

    try:

        imagen = imagen_producto_servicio.agregar_imagen(
            producto_id,
            archivo
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
        "message": "Imagen agregada con éxito.",
        "data": {
            "id": imagen.id,
            "producto_id": imagen.producto_id,
            "url_imagen": imagen.url_imagen,
            "orden": imagen.orden
        }
    }), 201


@admin_productos_bp.route(
    "/productos/<int:producto_id>/imagenes",
    methods=["GET"]
)
@admin_requerido
def listar_imagenes_producto(
    usuario_id,
    producto_id
):

    try:

        imagenes = (
            imagen_producto_servicio
            .listar_imagenes(
                producto_id
            )
        )

    except ValueError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    return jsonify({
        "success": True,
        "message": "Imágenes encontradas.",
        "data": [
            {
                "id": imagen.id,
                "producto_id": imagen.producto_id,
                "url_imagen": imagen.url_imagen,
                "orden": imagen.orden
            }
            for imagen in imagenes
        ]
    }), 200


@admin_productos_bp.route(
    "/productos/imagenes/<int:imagen_id>",
    methods=["DELETE"]
)
@admin_requerido
def eliminar_imagen_producto(
    usuario_id,
    imagen_id
):

    try:

        imagen_producto_servicio.eliminar_imagen(
            imagen_id
        )

    except ImagenProductoNoEncontradaError as err:

        return jsonify({
            "success": False,
            "error": {
                "message": str(err)
            }
        }), 404

    return jsonify({
        "success": True,
        "message": "Imagen eliminada con éxito."
    }), 200