from datetime import datetime

from app.extensions import db


class Pago(db.Model):

    __tablename__ = "pagos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    orden_id = db.Column(
        db.Integer,
        db.ForeignKey("ordenes.id"),
        nullable=False
    )

    referencia = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    monto = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    estado = db.Column(
        db.String(30),
        nullable=False,
        default="pendiente"
    )

    metodo = db.Column(
        db.String(50),
        nullable=True
    )

    id_transaccion = db.Column(
        db.String(100),
        nullable=True
    )

    fecha_creacion = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    fecha_actualizacion = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    orden = db.relationship(
        "Orden",
        backref=db.backref(
            "pagos",
            lazy=True
        )
    )

    def to_dict(self):

        return {
            "id": self.id,
            "orden_id": self.orden_id,
            "referencia": self.referencia,
            "monto": str(self.monto),
            "estado": self.estado,
            "metodo": self.metodo,
            "id_transaccion": self.id_transaccion,
            "fecha_creacion": (
                self.fecha_creacion.isoformat()
                if self.fecha_creacion
                else None
            ),
            "fecha_actualizacion": (
                self.fecha_actualizacion.isoformat()
                if self.fecha_actualizacion
                else None
            )
        }