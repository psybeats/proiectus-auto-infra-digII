from flask import Flask , Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager

app = Flask(__name__)

# Carga la Config
app.config.from_object("config.DevelopmentConfig")
csrf = CSRFProtect()
csrf.init_app(app)
db = SQLAlchemy(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


# Registra los Blueprint's
from app.views.auth import auth
from app.views.clinica import dentalShield
app.register_blueprint(auth)
app.register_blueprint(dentalShield)


db.create_all()

#from .models import Empleado
from app.models.empleado import Empleado


@login_manager.user_loader
def load_user(username_id):
    return Empleado.query.get(username_id)
    #return Empleado.query.filter_by(username_id=id).first()


# Excepciones u errores
def pagina_no_encontrada(error):
    return render_template("errores/404.html", mensaje=format(Exception)), 404


def pagina_no_autorizada(error):
    #return render_template("errores/error.html"), 401
    return redirect(url_for("auth.login", mensaje=format(Exception)), 401)
    #return redirect(url_for("login"))


app.register_error_handler(401, pagina_no_autorizada)

app.register_error_handler(404, pagina_no_encontrada)
