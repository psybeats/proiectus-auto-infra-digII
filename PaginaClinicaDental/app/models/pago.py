from app import db
from datetime import datetime


class Pago(db.Model):
    __tablename__ = "pagos"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    pagoTotal = db.Column(db.Float)
    notaPago = db.Column(db.String(250))
    idCitaPago = db.Column(db.Integer, db.ForeignKey("registroCitas.id"), nullable=False)
    idEmpleados = db.Column(db.Integer, db.ForeignKey("empleados.id"), nullable=False)

    def __init__(self, pagoTotal, notaPago) -> None:
        self.pagoTotal = pagoTotal
        self.notaPago = notaPago

    def __repr__(self) -> str:
        return f"User: {self.pagoTotal} {self.notaPago}"
