from app import db
from datetime import datetime


class Consultorio(db.Model):
    __tablename__ = "consultorios"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    horario = db.Column(db.String(20))

    def __init__(self, horario) -> None:
        self.horario = horario

    def __repr__(self) -> str:
        return f"User: {self.horario}"
