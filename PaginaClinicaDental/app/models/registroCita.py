from app import db
from datetime import datetime


class RegistroCita(db.Model):
    __tablename__ = "registroCitas"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombrePaciente = db.Column(db.String(20))
    apellidoPatPaciente = db.Column(db.String(25))
    apellidoMatPaciente = db.Column(db.String(25))
    edad = db.Column(db.Integer)
    telefono = db.Column(db.String(25))
    nota = db.Column(db.String(250))
    pagoTotalCitas = db.Column(db.Float)
    fechaRegistro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    estatus = db.Column(db.String(20))
    fechaCancelacion = db.Column(db.DateTime)
    idServicioRegis = db.Column(db.Integer, db.ForeignKey("servicios.id"), nullable=False)
    idServicioRegisDos = db.Column(db.Integer, db.ForeignKey("servicios.id"), nullable=False)
    idServicioRegisTres = db.Column(db.Integer, db.ForeignKey("servicios.id"), nullable=False)
    idClinicaRegis = db.Column(db.Integer, db.ForeignKey("clinicas.id"), nullable=False)
    idEmpleRegis = db.Column(db.Integer, db.ForeignKey("empleados.id"), nullable=True)
    idConsultorioReg = db.Column(db.Integer, db.ForeignKey("consultorios.id"), nullable=True)
    


    def __init__(self, nombrePaciente, apellidoPatPaciente, apellidoMatPaciente, edad, estatus, telefono, nota, fechaRegistro, fechaCancelacion, idServicioRegis, idServicioRegisDos, idServicioRegisTres, idClinicaRegis) -> None:
        self.nombrePaciente = nombrePaciente
        self.apellidoPatPaciente = apellidoPatPaciente
        self.apellidoMatPaciente = apellidoMatPaciente
        self.edad = edad
        self.estatus = estatus
        self.telefono = telefono
        self.nota = nota
        self.fechaRegistro = fechaRegistro
        self.fechaCancelacion = fechaCancelacion
        self.idServicioRegis = idServicioRegis
        self.idServicioRegisDos = idServicioRegisDos
        self.idServicioRegisTres = idServicioRegisTres
        self.idClinicaRegis = idClinicaRegis

    def __repr__(self) -> str:
        return f"User: {self.nombrePaciente} {self.apellidoPatPaciente} {self.apellidoMatPaciente} {self.edad} {self.estatus} {self.telefono} {self.nota} {self.fechaRegistro}"
