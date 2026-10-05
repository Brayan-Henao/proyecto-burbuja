from datetime import datetime

from app.extensions import db


class Usuario(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(255), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    rol = db.Column(db.String(20), nullable=False, server_default='usuario')

    def to_dict(self):
        return {
            "id": self.id,
            "correo": self.correo,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "rol": self.rol,
        }