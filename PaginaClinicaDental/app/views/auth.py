from flask import Flask , Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.empleado import Empleado
from app.models.rol import Rol
from app.models.servicio import Servicio
from app.models.registroCita import RegistroCita
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
        passwordV = request.form.get("passwordV")
        apellidoPAtEmpleado = request.form.get("apellidoPAtEmpleado")
        apellidoMatEmpleado = request.form.get("apellidoMatEmpleado")
        correoElectronico = request.form.get("correoElectronico")
        estadoEmpleado = request.form.get("estadoEmpleado")
        creado = None

        email_exists = Empleado.query.filter_by(correoElectronico=correoElectronico).first()
        username_exists = Empleado.query.filter_by(username=username).first()

        if email_exists:
            flash('El email utilizado ya esta registrado.', category='error')
        elif username_exists:
            flash('El nombre de usuario no esta disponible.', category='error')
        elif password != passwordV:
            flash('Las contraseñas no coinciden!', category='error')
        elif len(username) < 6:
            flash('El nombre de usuario es muy corto.', category='error')
        elif len(password) < 6:
            flash('La contraseña es muy corta.', category='error')
        elif len(correoElectronico) < 6:
            flash("El correo electrónico es invalido.", category='error')

        new_user = Empleado(
            username,
            apellidoPAtEmpleado,
            apellidoMatEmpleado,
            generate_password_hash(password, method='sha256'),
            correoElectronico,
            estadoEmpleado,
            creado,
        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash('¡Usuario creado!', category='success')
        return redirect(url_for('auth.login'))

    return render_template("auth/signup.html", user=current_user)


# /auth/login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = Empleado.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash(LOGGED_IN, category='success')
                login_user(user, remember=True)
                return redirect(url_for('DentalShield.index'))
                #return redirect(url_for('auth.login'))
            else:
                flash(LOGIN_PASSINVALIDA, category='error')
        else:
            flash(LOGIN_USERINVALIDO, category='error')

    flash(MENSAJE_BIENVENIDA, category='success')
    return render_template("auth/login.html", user=current_user)


# Para cerrar sesión
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(LOGOUT, category='success')
    return redirect(url_for('DentalShield.index'))