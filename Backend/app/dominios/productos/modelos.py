from datetime import datetime

from app.extensions import db


class Producto(db.Model):

    __tablename__ = "productos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(150),
        nullable=False
    )

    descripcion = db.Column(
        db.Text,
        nullable=False
    )

    precio = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    stock = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    disponible = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    categoria = db.Column(
        db.String(100),
        nullable=False
    )

    min_fotos = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    max_fotos = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    permite_grabado = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    max_caracteres_grabado = db.Column(
        db.Integer,
        nullable=True
    )

    precio_grabado = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
    )

    permite_tarjeta = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    max_caracteres_tarjeta = db.Column(
        db.Integer,
        nullable=True
    )

    fecha_creacion = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    imagenes = db.relationship(
        "ImagenProducto",
        backref="producto",
        lazy=True,
        cascade="all, delete-orphan"
    )

    opciones = db.relationship(
        "OpcionProducto",
        backref="producto",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):

        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": str(self.precio),
            "stock": self.stock,
            "disponible": self.disponible,
            "categoria": self.categoria,
            "min_fotos": self.min_fotos,
            "max_fotos": self.max_fotos,
            "permite_grabado": self.permite_grabado,
            "max_caracteres_grabado": self.max_caracteres_grabado,
            "precio_grabado": str(self.precio_grabado),
            "permite_tarjeta": self.permite_tarjeta,
            "max_caracteres_tarjeta": self.max_caracteres_tarjeta,
            "fecha_creacion": (
                self.fecha_creacion.isoformat()
                if self.fecha_creacion
                else None
            ),
            "imagenes": [
                {
                    "id": imagen.id,
                    "url_imagen": imagen.url_imagen,
                    "orden": imagen.orden
                }
                for imagen in self.imagenes
            ]
        }


class ImagenProducto(db.Model):

    __tablename__ = "imagenes_productos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    producto_id = db.Column(
        db.Integer,
        db.ForeignKey("productos.id"),
        nullable=False
    )

    url_imagen = db.Column(
        db.String(500),
        nullable=False
    )

    orden = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )