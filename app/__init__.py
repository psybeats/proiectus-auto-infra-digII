from flask import Flask
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# Carga la Config
app.config.from_object("config.DevelopmentConfig")
csrf = CSRFProtect()
csrf.init_app(app)
db = SQLAlchemy(app)

# Importa Vistas
from app.views.auth import lazuli

app.register_blueprint(lazuli)

db.create_all()


# Excepciones u errores
def pagina_no_encontrada(error):
    return render_template('errores/404.html'), 404


def pagina_no_autorizada(error):
    return redirect(url_for('login'))


app.register_error_handler(401, pagina_no_autorizada)

app.register_error_handler(404, pagina_no_encontrada)
