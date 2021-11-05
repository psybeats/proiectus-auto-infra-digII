from app import db


class Rol(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)
    tipoRol = db.Column(db.String(20))

    def __init__(self, tipoRol) -> None:
        self.tipoRol = tipoRol

    def __repr__(self) -> str:
        return f"User: {self.tipoRol}"
