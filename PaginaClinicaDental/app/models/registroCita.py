from app import db
from datetime import datetime


class RegistroCita(db.Model):
    __tablename__ = "registroCitas"
    id = db.Column(db.Integer(), primary_key=True)
    nombrePaciente = db.Column(db.String(20))
    apellidoPatPaciente = db.Column(db.String(25))
    apellidoMatPaciente = db.Column(db.String(25))
    edad = db.Column(db.Integer)
    telefono = db.Column(db.String(25))
    estado = db.Column(db.String(8))
    costo = db.Column(db.Float)
    nota = db.Column(db.String(25))
    fechaRegistro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    idServicioRegis = db.Column(db.Integer, db.ForeignKey("servicios.id"), nullable=False)
    idConsultorioReg = db.Column(db.Integer, db.ForeignKey("consultorios.id"), nullable=False)
    idClinicaRegis = db.Column(db.Integer, db.ForeignKey("clinicas.id"), nullable=False)
    idEmpleRegis = db.Column(db.Integer, db.ForeignKey("empleados.id"), nullable=False)

    def __init__(self, nombrePaciente, apellidoPatPaciente, apellidoMatPaciente, edad, telefono, estado, costo, nota, fechaRegistro) -> None:
        self.nombrePaciente = nombrePaciente
        self.apellidoPatPaciente = apellidoPatPaciente
        self.apellidoMatPaciente = apellidoMatPaciente
        self.edad = edad
        self.telefono = telefono
        self.estado = estado
        self.costo = costo
        self.nota = nota
        self.fechaRegistro = fechaRegistro

    def __repr__(self) -> str:
        return f"User: {self.nombrePaciente} {self.edad} {self.fechaRegistro} {self.costo} {self.estado}"
