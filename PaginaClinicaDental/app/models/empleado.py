from app import db
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin


class Empleado(UserMixin, AnonymousUserMixin, db.Model):
    __tablename__ = "empleados"
    idEmpleado = db.Column(db.Integer, primary_key=True)
    nombreEmpleado = db.Column(db.String(20), nullable=False)
    apellidoPAtEmpleado = db.Column(db.String(25))
    apellidoMatEmpleado = db.Column(db.String(25))
    cedulaProfesional = db.Column(db.String(40))
    #password = db.Column(db.String(255))
    contraseña = db.Column(db.String(250))
    correoElectronico = db.Column(db.String(150), unique=True, nullable=False)
    estadoEmpleado = db.Column(db.String(8))
    idConsultorioEmple = db.Column(db.Integer, db.ForeignKey("consultorios.claveC1"))
    idClinicaEmpleado = db.Column(db.Integer, db.ForeignKey("clinicas.idClinica"))
    idRolEmpleado = db.Column(db.Integer, db.ForeignKey("roles.idRol"))


    def __init__(self, nombreEmpleado, apellidoPAtEmpleado, apellidoMatEmpleado, cedulaProfesional, contraseña, correoElectronico, estadoEmpleado, creado,) -> None:
        self.nombreEmpleado = nombreEmpleado
        self.apellidoPAtEmpleado = apellidoPAtEmpleado
        self.apellidoMatEmpleado = apellidoMatEmpleado
        self.cedulaProfesional = cedulaProfesional
        self.contraseña = contraseña
        self.correoElectronico = correoElectronico
        self.estadoEmpleado = estadoEmpleado
        self.creado = creado

    def __repr__(self) -> str:
        return f"User: {self.nombreEmpleado} {self.correoElectronico}"
