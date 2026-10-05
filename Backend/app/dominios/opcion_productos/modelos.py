from app.extensions import db


class OpcionProducto(db.Model):
    __tablename__ = "opciones_productos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    producto_id = db.Column(
        db.Integer,
        db.ForeignKey("productos.id"),
        nullable=False
    )

    tipo = db.Column(
        db.String(50),
        nullable=False
    )

    valor = db.Column(
        db.String(100),
        nullable=False
    )

    activa = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    opcion_principal_id = db.Column(
        db.Integer,
        db.ForeignKey("opciones_productos.id"),
        nullable=True
    )

    opciones_dependientes = db.relationship(
        "OpcionProducto",
        backref=db.backref(
            "opcion_principal",
            remote_side=[id]
        ),
        lazy=True
    )