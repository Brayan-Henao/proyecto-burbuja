from datetime import datetime

from app.extensions import db


class Orden(db.Model):

    __tablename__ = "ordenes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    estado = db.Column(
        db.String(30),
        nullable=False,
        default="pendiente"
    )

    subtotal = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
    )

    envio_minimo = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
    )

    envio_maximo = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
    )

    fecha_creacion = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    items = db.relationship(
        "OrdenItem",
        backref="orden",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):

        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "estado": self.estado,
            "subtotal": str(self.subtotal),
            "envio_minimo": str(self.envio_minimo),
            "envio_maximo": str(self.envio_maximo),
            "fecha_creacion": (
                self.fecha_creacion.isoformat()
                if self.fecha_creacion
                else None
            )
        }


class OrdenItem(db.Model):

    __tablename__ = "ordenes_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    orden_id = db.Column(
        db.Integer,
        db.ForeignKey("ordenes.id"),
        nullable=False
    )

    producto_id = db.Column(
        db.Integer,
        db.ForeignKey("productos.id"),
        nullable=False
    )

    personalizacion_id = db.Column(
        db.Integer,
        db.ForeignKey("personalizaciones.id"),
        nullable=True
    )

    cantidad = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    precio_unitario = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    precio_grabado = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
    )

    subtotal = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    def to_dict(self):

        return {
            "id": self.id,
            "orden_id": self.orden_id,
            "producto_id": self.producto_id,
            "personalizacion_id": self.personalizacion_id,
            "cantidad": self.cantidad,
            "precio_unitario": str(self.precio_unitario),
            "precio_grabado": str(self.precio_grabado),
            "subtotal": str(self.subtotal)
        }