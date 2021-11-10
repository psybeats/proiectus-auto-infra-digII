from flask import Flask , Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify

from werkzeug.exceptions import abort

from flask_login import login_required, current_user
from app.mensajesflash import *


from app.models.empleado import Empleado
from app.models.rol import Rol
from app.models.servicio import Servicio
from app.models.registroCita import RegistroCita
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
        flash(MENSAJE_USER, category='success')
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
            flash(MENSAJE_USER, category='success')
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

        servicio = Servicio(nombreServicio, costoServicio)

        error = None
        if not nombreServicio:
            error = "Se requiere un nombre del servicio"
        elif not costoServicio:
            error = "Se requiere un costo de servicio"
        else:
            flash(NOTSERVICES, category='error')

        if error is not None:
            flash(error, category='error')
        else:
            db.session.add(servicio)
            db.session.commit()
            flash(MENSAJE, category='success')
            #return redirect(url_for("DentalShield.index"))
            return redirect(url_for("DentalShield.servicios"))

    return render_template("clinica/servicios.html", user=current_user)
 

@dentalShield.route("/DentalShield/servicios-creados")
@login_required
def viewservicios():
    servicios = Servicio.query.all()
    flash(MENSAJE, category='success')
    return render_template("clinica/serviciosC.html", user=current_user, servicios=servicios)

#Registro de Citas
@dentalShield.route("/DentalShield/citas", methods=["GET", "POST"])
def citas():
    posts = Servicio.query.all()
    clinica = Clinica.query.all()
    if request.method == "POST":
        nombrePaciente = request.form.get("nombrePaciente")
        apellidoPatPaciente = request.form.get("apellidoPatPaciente")
        apellidoMatPaciente = request.form.get("apellidoMatPaciente")
        edad = request.form.get("edad")
        estatus = "Activo"
        telefono = request.form.get("telefono")
        nota = request.form.get("nota")
        fechaRegistro = request.form.get("fechaRegistro")
        fechaCancelacion = request.form.get("fechaCancelacion")
        idServicioRegis = request.form.get("nombreServicio")
        idClinicaRegis = request.form.get("idClinicaRegis")
        


        registro = RegistroCita(nombrePaciente, apellidoPatPaciente, apellidoMatPaciente, edad, estatus, telefono, nota, fechaRegistro, fechaCancelacion, idServicioRegis, idClinicaRegis)

        error = None
        if not nombrePaciente:
            error = "Se requiere un nombre del paciente"
        elif not apellidoPatPaciente:
            error = "Se requiere el apellido paterno del paciente"
        elif not apellidoMatPaciente:
            error = "Se requiere el apellido materno del paciente"
        elif not edad:
            error = "Se requiere la edad del paciente"
        elif not telefono:
            error = "Se requiere el teléfono del paciente"
        elif not fechaRegistro:
            error = "Se requiere una fecha de registro"

        if error is not None:
            flash(error)
        else:
            db.session.add(registro)
            db.session.commit()
            return redirect(url_for("DentalShield.citas"))

    return render_template("clinica/citas.html", posts=posts, clinica=clinica)