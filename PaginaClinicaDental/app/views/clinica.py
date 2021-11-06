from flask import Flask , Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify

from werkzeug.exceptions import abort

from flask_login import login_required, current_user
from app.mensajesflash import *


from app.models.empleado import Empleado
from app.models.rol import Rol
from app.models.servicio import Servicio
from app.models.registroCita import RegistroCita
from app.models.cancelacion import Cancelacion
from app.models.pago import Pago
from app.models.consultorio import Consultorio
from app.models.clinica import Clinica


from app import db


# lazuli = Blueprint("lazuli", __name__, url_prefix="/clinica")
dentalShield = Blueprint("DentalShield", __name__,)


# Inicio del sistema web
@dentalShield.route("/")
def index():
    try:
        return render_template('clinica/index.html', user=current_user)
    except Exception as ex:
        return render_template('errores/error.html', mensaje=format(ex))
    else:
        return redirect(url_for('auth.login'))
    finally:
        pass

    #return render_template('clinica/index.html', user=current_user)


@dentalShield.route("/DentalShield/perfil")
@login_required
def perfil():
    if current_user.is_authenticated:
        try:
            return render_template('clinica/perfil.html', user=current_user)
        except Exception as ex:
            return render_template('errores/error.html', mensaje=format(ex))
        else:
            return redirect(url_for('auth.login'))
        finally:
            pass
    #return render_template('clinica/perfil.html', user=current_user)


# Registrar un servicio
@dentalShield.route("/DentalShield/crear-servicio", methods=["GET", "POST"])
@login_required
def servicios():
    if request.method == "POST":
        nombreServicio = request.form.get("nombreServicio")
        costoServicio = request.form.get("costoServicio")
        #user = current_user

        servicio = Servicio(nombreServicio, costoServicio)

        error = None
        if not nombreServicio:
            error = "Se requiere un nombre del servicio"
        elif not costoServicio:
            error = "Se requiere un costo de servicio"
        else:
            pass
            # print("Error")

        if error is not None:
            flash(error)
        else:
            db.session.add(servicio)
            db.session.commit()
            flash('Servicio creado!', category='success')
            #return redirect(url_for("DentalShield.index"))
            return redirect(url_for("DentalShield.servicios"))

        flash(error)
        #flash(correct)

    return render_template("clinica/servicios.html", user=current_user)


@dentalShield.route("/DentalShield/servicios-creados")
@login_required
def verservicios():
    servicios = Servicio.query.all()
    return render_template("clinica/serviciosC.html", user=current_user, servicios=servicios)