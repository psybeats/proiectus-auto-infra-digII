from app import db


class Clinica(db.Model):
    __tablename__ = "clinicas"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    nombreClinica = db.Column(db.String(40))
    direcccion = db.Column(db.String(100))
    telefono = db.Column(db.String(25))

    def __init__(self, nombreClinica, direcccion, telefono) -> None:
        self.nombreClinica = nombreClinica
        self.direcccion = direcccion
        self.telefono = telefono

    def __repr__(self) -> str:
        return f"User: {self.nombreClinica} {self.direcccion}"
