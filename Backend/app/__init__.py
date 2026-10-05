from flask import Flask, send_from_directory

from flask_cors import CORS

from app.config import Config

from app.extensions import db, migrate


# Modelos

from app.dominios.usuarios.modelos import Usuario

from app.dominios.productos.modelos import (
    Producto,
    ImagenProducto
)

from app.dominios.opcion_productos.modelos import (
    OpcionProducto
)

from app.dominios.personalizaciones.modelos import (
    Personalizacion,
    FotoPersonalizacion,
    OpcionPersonalizacion
)

from app.dominios.ordenes.modelos import (
    Orden,
    OrdenItem
)

from app.dominios.pagos.modelos import (
    Pago
)


# Controladores

from app.dominios.usuarios.controladores import (
    usuarios_bp,
    admin_bp
)

from app.dominios.productos.controladores import (
    productos_bp,
    admin_productos_bp
)

from app.dominios.opcion_productos.controladores import (
    opciones_productos_bp
)

from app.dominios.personalizaciones.controladores import (
    personalizaciones_bp
)

from app.dominios.ordenes.controladores import (
    ordenes_bp
)

from app.dominios.pagos.controladores import (
    pagos_bp
)


# Servicios de usuarios

from app.dominios.usuarios.servicios import (
    UsuarioServicio,
    PermisoDenegadoError
)

from app.dominios.usuarios import (
    controladores as usuarios_ctrl
)


# Servicios de productos

from app.dominios.productos.servicios import (
    ProductoServicio
)

from app.dominios.productos import (
    controladores as productos_ctrl
)


def crear_app():

    app = Flask(__name__)


    # ==========================================
    # CARGAR CONFIGURACIÓN
    # ==========================================

    app.config.from_object(
        Config
    )


    # ==========================================
    # INICIALIZAR EXTENSIONES
    # ==========================================

    db.init_app(app)

    migrate.init_app(
        app,
        db
    )

    CORS(app)


    # ==========================================
    # CONECTAR SERVICIO DE USUARIOS
    # ==========================================

    usuarios_ctrl.usuario_servicio = UsuarioServicio(
        secret_key=app.config["SECRET_KEY"],
        jwt_exp_minutes=app.config.get(
            "JWT_EXP_MINUTES",
            15
        )
    )


    # ==========================================
    # CONECTAR SERVICIO DE PRODUCTOS
    # ==========================================

    productos_ctrl.producto_servicio = ProductoServicio()


    # ==========================================
    # REGISTRAR BLUEPRINTS
    # ==========================================

    # Usuarios

    app.register_blueprint(
        usuarios_bp,
        url_prefix="/api/v1/usuarios"
    )


    # Administración de usuarios

    app.register_blueprint(
        admin_bp,
        url_prefix="/api/v1/admin"
    )


    # Productos públicos

    app.register_blueprint(
        productos_bp,
        url_prefix="/api/v1/productos"
    )


    # Productos para administración

    app.register_blueprint(
        admin_productos_bp,
        url_prefix="/api/v1/admin"
    )


    # Opciones de productos

    app.register_blueprint(
        opciones_productos_bp,
        url_prefix="/api/v1/opciones-productos"
    )


    # Personalizaciones

    app.register_blueprint(
        personalizaciones_bp,
        url_prefix="/api/v1/personalizaciones"
    )


    # Órdenes

    app.register_blueprint(
        ordenes_bp,
        url_prefix="/api/v1/ordenes"
    )


    # Pagos

    app.register_blueprint(
        pagos_bp,
        url_prefix="/api/v1/pagos"
    )


    # ==========================================
    # ARCHIVOS SUBIDOS
    # ==========================================

    @app.route(
        "/uploads/<path:nombre_archivo>"
    )
    def servir_archivo(nombre_archivo):

        return send_from_directory(
            app.config["UPLOAD_FOLDER"],
            nombre_archivo
        )


    # ==========================================
    # RUTA DE SALUD
    # ==========================================

    @app.route("/health")

    def health():

        return {
            "status": "ok",
            "mensaje": (
                "Burbuja backend funcionando"
            )
        }


    # ==========================================
    # MANEJO DE PERMISOS
    # ==========================================

    @app.errorhandler(
        PermisoDenegadoError
    )
    def manejar_permiso_denegado(error):

        return {
            "success": False,
            "error": {
                "message": str(error)
            }
        }, 403


    return app