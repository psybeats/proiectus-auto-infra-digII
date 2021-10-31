from flask import render_template, Blueprint, flash, g, redirect, request, url_for
from werkzeug.exceptions import abort
from app.models.servicio import Servicio
from app.models.empleado import Empleado
from app.views.auth import login_required

from app import db


# lazuli = Blueprint("lazuli", __name__, url_prefix="/tlantisitl")
tlantisitl = Blueprint("tlantisitl", __name__,)


# Obtiene la sesion del usuario
def get_user(id):
    user = Empleado.query.get_or_404(id)
    return user


@tlantisitl.route("/")
def index():
    servicios = Servicio.query.all()
    db.session.commit()
    # return render_template('tlantisitl/index.html', servicios = servicios)
    return redirect(url_for("auth.login"))


# Registrar un servicio
@tlantisitl.route("/tlantisitl/crear-servicio", methods=["GET", "POST"])
@login_required
def servicios():
    if request.method == "POST":
        nombreServicio = request.form.get("nombreServicio")
        costoServicio = request.form.get("costoServicio")

        servicio = Servicio(g.user.id, nombreServicio, costoServicio)

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
            return redirect(url_for("tlantisitl.servicios"))

        flash(error)

    return render_template("tlantisitl/servicios.html")
