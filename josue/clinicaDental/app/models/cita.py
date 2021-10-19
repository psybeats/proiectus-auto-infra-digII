from app import db
from datetime import datetime

class Cita(db.Model):
    __tablename__ = 'citas'
    id_cita = db.Column(db.Integer, primary_key=True)
    nombre_paciente = db.Column(db.String(50), db.ForeignKey('paciente'), nullable=False)
    titulo = db.Column(db.String(35))
    cuerpo = db.Column(db.Text)
    fecha = db.Column(db.DATETIME, nullable=False, default=datetime.utcnow)

    def __init__(self, id_cita, nombre_paciente, titulo, cuerpo, fecha) -> None:
        self.id_cita = id_cita
        self.nombre_paciente = nombre_paciente
        self.titulo = titulo
        self.cuerpo = cuerpo
        self.fecha = fecha

    def __repr__(self) -> str:
        return f'Cita: {self.id_cita} {self.nombre_paciente} {self.titulo} {self.cuerpo} {self.fecha}'