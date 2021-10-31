from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

from app.models.empleado import Empleado
from app.models.rol import Rol
from app.models.servicio import Servicio
from app.models.registroCita import RegistroCita
from app.models.cancelacion import Cancelacion
from app.models.pago import Pago
from app.models.consultorio import Consultorio
from app.models.clinica import Clinica

import functools

from werkzeug.security import check_password_hash, generate_password_hash
from app import db

auth = Blueprint("auth", __name__, url_prefix="/auth")

# Registros (BLUEPRINTS)


@auth.route("/prueba")
def prueba():
    return "¡Hello, World!"


@auth.route("/")
def index():
    return "🥵"


# /auth/register
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        apellidoPAtEmpleado = request.form.get("apellidoPAtEmpleado")
        apellidoMatEmpleado = request.form.get("apellidoMatEmpleado")
        correoElectronico = request.form.get("correoElectronico")
        cedulaProfesional = request.form.get("cedulaProfesional")
        estadoEmpleado = request.form.get("estadoEmpleado")
        creado = None

        user = Empleado(
            username,
            apellidoPAtEmpleado,
            apellidoMatEmpleado,
            cedulaProfesional,
            generate_password_hash(password),
            correoElectronico,
            estadoEmpleado,
            creado,
        )

        error = None
        if not username:
            error = "Se requiere nombre de usuario"
        elif not apellidoPAtEmpleado:
            error = "Se requiere apellido paterno"
        elif not apellidoMatEmpleado:
            error = "Se requiere apellido materno"
        elif not correoElectronico:
            error = "Se requiere un correo electrónico"
        elif not estadoEmpleado:
            error = "Se requiere un estado para el empleado"
        elif not password:
            error = "Se requiere una contraseña"
        else:
            pass
            # print("Error")

        user_name = Empleado.query.filter_by(username=username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            # return redirect(url_for('auth.login'))
        else:
            error = f"El usuario ya {username} esta registrado"
        flash(error)

    return render_template("auth/register.html")


# /auth/login
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        error = None

        user = Empleado.query.filter_by(username=username).first()

        if user == None:
            error = "Nombre de usuario incorrecto"
        elif not check_password_hash(user.password, password):
            error = "Contraseña es incorrecta"
        else:
            pass
            # print("Error")

        if error is None:
            session.clear()
            session["user_id"] = user.id
            # return redirect(url_for('index'))
            # return redirect(url_for('tlantisitl.servicios'))

        flash(error)

    return render_template("auth/login.html")


# load_logged_in_user
@auth.before_app_request
def load_logged_in_user():
    user_id = session.get("user.id")

    if user_id is None:
        g.user = None
    else:
        g.user = Empleado.query.get_or_404(user_id)


# load_logged_in_user
@auth.route("/logout")
def logout():
    session.clear()
    # return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_wiew(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_wiew
