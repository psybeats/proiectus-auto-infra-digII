from app import db


class Servicio(db.Model):
    __tablename__ = "servicios"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    nombreServicio = db.Column(db.String(50))
    costoServicio = db.Column(db.Float)

    def __init__(self, nombreServicio, costoServicio) -> None:
        self.nombreServicio = nombreServicio
        self.costoServicio = costoServicio

    def __repr__(self) -> str:
        return f"User: {self.nombreServicio} {self.costoServicio}"
