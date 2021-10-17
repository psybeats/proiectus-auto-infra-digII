from app import db

class Cargo(db.Model):
    __tablename__ = 'cargos'
    id_cargo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.VARCHAR(30))

    def __init__(self, id_cargo, nombre) -> None:
        self.id_cargo = id_cargo
        self.nombre = nombre

    def __repr__(self) -> str:
        return f'Cargo: {self.id_cargo} {self.nombre}'