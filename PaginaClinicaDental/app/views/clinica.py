from flask import Flask , Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify

from werkzeug.exceptions import abort

from flask_login import login_required, current_user

from app.models.empleado import Empleado
from app.models.servicio import Servicio


from app import db


# lazuli = Blueprint("lazuli", __name__, url_prefix="/clinica")
dentalShield = Blueprint("DentalShield", __name__,)


# Inicio del sistema web
@dentalShield.route("/")
def index():
    #servicios = Servicio.query.all()
    #db.session.commit()
    #return render_template('clinica/index.html', servicios = servicios)
    return render_template('clinica/index.html')
    #return redirect(url_for("auth.login"))


@dentalShield.route("/perfil")
@login_required
def perfil():
    #return render_template('clinica/perfil.html', name=current_user.name)
    return render_template('clinica/perfil.html', name=g.user.id)


# Registrar un servicio
@dentalShield.route("/DentalShield/crear-servicio", methods=["GET", "POST"])
@login_required
def servicios():
    if request.method == "POST":
        nombreServicio = request.form.get("nombreServicio")
        costoServicio = request.form.get("costoServicio")

        servicio = Servicio(g.user.id, nombreServicio, costoServicio)

        error = None
        correct = 'Servicio creado satisfactoriamente 😎'
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
            #return redirect(url_for("DentalShield.index"))
            return redirect(url_for("DentalShield.servicios"))

        flash(error)
        flash(correct)

    return render_template("clinica/servicios.html")
