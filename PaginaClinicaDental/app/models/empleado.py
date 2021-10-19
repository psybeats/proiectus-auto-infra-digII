from app import db

class Empleado(db.Model):
    __tablename__ = 'empleados'
    id_empleado = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    contrasena = db.Column(db.Text)
    email = db.Column(db.String(50))

    def __init__(self, nombre, contrasena, email) -> None:
        self.nombre = nombre
        self.contrasena = contrasena
        self.email = email

    def __repr__(self) -> str:
        return f'User: {self.nombre} {self.email}'