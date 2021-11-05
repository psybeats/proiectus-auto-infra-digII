from app import db
from datetime import datetime


class Cancelacion(db.Model):
    __tablename__ = "cancelaciones"
    id = db.Column(db.Integer(), primary_key=True)
    telefono = db.Column(db.String(20))
    nota = db.Column(db.String(25))
    fechaCancelacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    idCitaCancelar = db.Column(db.Integer, db.ForeignKey("registroCitas.id"), nullable=False)

    def __init__(self, telefono, nota, fechaCancelacion) -> None:
        self.telefono = telefono
        self.nota = nota
        self.fechaCancelacion = fechaCancelacion

    def __repr__(self) -> str:
        return f"User: {self.telefono} {self.nota} {self.fechaCancelacion}"
