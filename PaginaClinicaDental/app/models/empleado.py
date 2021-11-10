from app import db
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin


class Empleado(UserMixin, AnonymousUserMixin, db.Model):
    __tablename__ = "empleados"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    apellidoPAtEmpleado = db.Column(db.String(25))
    apellidoMatEmpleado = db.Column(db.String(25))
    #password = db.Column(db.String(255))
    password = db.Column(db.Text)
    correoElectronico = db.Column(db.String(150), unique=True, nullable=False)
    estadoEmpleado = db.Column(db.String(8))
    creado = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    idConsultorioEmple = db.Column(db.Integer, db.ForeignKey("consultorios.id"))
    idClinicaEmpleado = db.Column(db.Integer, db.ForeignKey("clinicas.id"))
    idRolEmpleado = db.Column(db.Integer, db.ForeignKey("roles.id"))


    def __init__(self, username, apellidoPAtEmpleado, apellidoMatEmpleado, password, correoElectronico, estadoEmpleado, creado,) -> None:
        self.username = username
        self.apellidoPAtEmpleado = apellidoPAtEmpleado
        self.apellidoMatEmpleado = apellidoMatEmpleado
        self.password = password
        self.correoElectronico = correoElectronico
        self.estadoEmpleado = estadoEmpleado
        self.creado = creado

    def __repr__(self) -> str:
        return f"User: {self.username} {self.correoElectronico}"
