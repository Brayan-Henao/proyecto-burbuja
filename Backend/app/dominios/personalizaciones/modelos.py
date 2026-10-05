from datetime import datetime

from app.extensions import db


class Personalizacion(db.Model):
    __tablename__ = "personalizaciones"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    producto_id = db.Column(
        db.Integer,
        db.ForeignKey("productos.id"),
        nullable=False
    )

    grabado = db.Column(
        db.String(500),
        nullable=True
    )

    mensaje = db.Column(
        db.String(1000),
        nullable=True
    )

    fecha_creacion = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    fotos = db.relationship(
        "FotoPersonalizacion",
        backref="personalizacion",
        lazy=True,
        cascade="all, delete-orphan"
    )

    opciones = db.relationship(
        "OpcionPersonalizacion",
        backref="personalizacion",
        lazy=True,
        cascade="all, delete-orphan"
    )


class FotoPersonalizacion(db.Model):
    __tablename__ = "fotos_personalizaciones"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    personalizacion_id = db.Column(
        db.Integer,
        db.ForeignKey("personalizaciones.id"),
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


class OpcionPersonalizacion(db.Model):
    __tablename__ = "opciones_personalizaciones"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    personalizacion_id = db.Column(
        db.Integer,
        db.ForeignKey("personalizaciones.id"),
        nullable=False
    )

    opcion_producto_id = db.Column(
        db.Integer,
        db.ForeignKey("opciones_productos.id"),
        nullable=False
    )