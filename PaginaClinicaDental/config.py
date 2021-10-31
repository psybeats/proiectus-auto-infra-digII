class Config:
    # Configuración de FLASK
    SECRET_KEY = "6f96245812e53569545bubbles2e8c9c202ef495c40a197ca73783a56217abf10"
    DEBUG = False
    TESTING = False
    # Configuración de la DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ("mysql+pymysql://root:Donitas342@localhost:3306/clinica_dental")


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "default": DevelopmentConfig,
}
