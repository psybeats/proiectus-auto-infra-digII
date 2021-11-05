from flask import Flask , Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.empleado import Empleado
from app.models.rol import Rol
from app.models.servicio import Servicio
from app.models.registroCita import RegistroCita
from app.models.cancelacion import Cancelacion
from app.models.pago import Pago
from app.models.consultorio import Consultorio
from app.models.clinica import Clinica


import functools
from app.mensajesflash import *


from flask_login import login_user, logout_user, login_required, current_user
from app import db


auth = Blueprint("auth", __name__, url_prefix="/auth")


# Registros (BLUEPRINTS)


# /auth/register
@auth.route("/signup", methods=["GET", "POST"])
def signup():
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
            generate_password_hash(password , method='sha256'),
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

        if user_name is None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f"El usuario ya {username} esta registrado"
        flash(error)

    return render_template("auth/signup.html")


# /auth/login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        error = None

        user = Empleado.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login password and try again.')
            return redirect(url_for('auth.login'))

        login_user(user)
    #return redirect(url_for('DentalShield.perfil'))
    #return render_template("clinica/index.html")
    return render_template("auth/login.html")
    #return render_template("DentalShield.index")


# Para cerrar sesión
@auth.route('/logout')
@login_required
def logout():
    #session.clear()
    logout_user()
    flash("Sesión cerrada exitosamente!")
    return redirect(url_for('DentalShield.index'))

