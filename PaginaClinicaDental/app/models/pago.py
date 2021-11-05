from app import db
from datetime import datetime


class Pago(db.Model):
    __tablename__ = "pago"
    idPago = db.Column(db.Integer(), primary_key=True)
    pagoTotal = db.Column(db.Float)
    notaPago = db.Column(db.String(250))
    idCitaPago = db.Column(db.Integer, db.ForeignKey("registroCitas.idCitas"), nullable=False)

    def __init__(self, pagoTotal, notaPago) -> None:
        self.pagoTotal = pagoTotal
        self.notaPago = notaPago

    def __repr__(self) -> str:
        return f"User: {self.pagoTotal} {self.notaPago}"
