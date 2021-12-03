from flask import Flask , Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from fpdf import FPDF
from sqlalchemy.orm import joinedload

from werkzeug.exceptions import abort
import pymysql
from flask_login import login_required, current_user
from app.mensajesflash import *


from app.models.empleado import Empleado
from app.models.rol import Rol
from app.models.servicio import Servicio
from app.models.registroCita import RegistroCita
from app.models.pago import Pago
from app.models.consultorio import Consultorio
from app.models.clinica import Clinica

import createPROCESOS as p

from app import db

#mydb = pymysql.Connection(host="localhost", user="root", password="Donitas342", database="clinica_dental")
#mycursor = mydb.cursor()

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

#about
@dentalShield.route("/DentalShield/about")
def about():
    return render_template("clinica/about.html", user=current_user)


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
        if error is not None:
            flash(error)
        else:
            db.session.add(servicio)
            db.session.commit()
            flash(MENSAJE, category='success')
            #return redirect(url_for("DentalShield.index"))
            return redirect(url_for("DentalShield.servicios"))

    return render_template("clinica/servicios.html", user=current_user)
 

@dentalShield.route("/DentalShield/servicios-creados")

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
        estatus = "Cita Activa"
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

            #CAUSA FALLAS, SOLUCIONAR!
            p.random_registroCitas()
            p.crear_pagos()
            

            return redirect(url_for("DentalShield.citas"))

    return render_template("clinica/citas.html", posts=posts, clinica=clinica, user=current_user)


#--------------------- Cancelar Citas
@dentalShield.route("/DentalShield/cancelarcitas/<int:id>" , methods=["GET", "POST"])
@login_required
def cancelarcitas(id):
    cancita = db.session.query(RegistroCita).filter(RegistroCita.id == id).first()

    if request.method == "POST":
        updatestatus = request.form["estatus"]
        fechacan = request.form["fechaCancelacion"]


        error = None
        if not updatestatus:
            error = "Se requiere un estatus"
        elif not fechacan:
            error = "Se requiere una fecha de cancelacion"

        if error is not None:
            flash(error)
        else:
            cancita.estatus = updatestatus
            cancita.fechaCancelacion = fechacan

            db.session.add(cancita)
            db.session.commit()
            return redirect(url_for("DentalShield.viewcitas"))

    return render_template("clinica/cancelarCitas.html", user=current_user, cancita=cancita)

#--------------------- Update Registro Citas 
@dentalShield.route("/DentalShield/updatecitas/<int:id>", methods=["GET", "POST"])
@login_required
def updatecitas(id):
    posts = Servicio.query.all()
    clinica = Clinica.query.all()
    ucita =db.session.query(RegistroCita).filter(RegistroCita.id == id).first()
    
    resulCita = db.session.query(RegistroCita, Empleado, Servicio, Consultorio, Clinica 
    ).filter(RegistroCita.idEmpleRegis == Empleado.id,
    RegistroCita.idServicioRegis == Servicio.id,
    RegistroCita.idConsultorioReg == Consultorio.id,
    RegistroCita.idClinicaRegis == Clinica.id).all()

    if request.method == "POST":
        
        nombrePaciente = request.form.get("nombrePaciente")
        apellidoPatPaciente = request.form.get("apellidoPatPaciente")
        apellidoMatPaciente = request.form.get("apellidoMatPaciente")
        edad = request.form.get("edad")
        telefono = request.form.get("telefono")
        nota = request.form.get("nota")
        fechaRegistro = request.form.get("fechaRegistro")
        idServicioRegis = request.form.get("nombreServicio")
        idClinicaRegis = request.form.get("idClinicaRegis")


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
            ucita.nombrePaciente = nombrePaciente
            ucita.apellidoPatPaciente = apellidoPatPaciente
            ucita.apellidoMatPaciente = apellidoMatPaciente
            ucita.edad = edad 
            ucita.telefono = telefono
            ucita.nota = nota 
            ucita.fechaRegistro = fechaRegistro
            ucita.idServicioRegis = idServicioRegis
            ucita.idClinicaRegis = idClinicaRegis

            db.session.add(ucita)
            db.session.commit()
            return redirect(url_for("DentalShield.viewcitas"))

    return render_template("clinica/updatecitas.html", user=current_user, ucita=ucita, posts=posts, clinica=clinica, resulCita=resulCita)


#------------------------------------------------------------Citas Registradas
@dentalShield.route("/DentalShield/citas-registradas")
@login_required
def viewcitas():
    resulCita = db.session.query(RegistroCita, Empleado, Servicio, Consultorio, Clinica 
    ).filter(
    RegistroCita.idEmpleRegis == Empleado.id,
    RegistroCita.idServicioRegis == Servicio.id,
    RegistroCita.idConsultorioReg == Consultorio.id,
    RegistroCita.idClinicaRegis == Clinica.id).all()

    return render_template("clinica/vistaCitas.html", user=current_user, resulCita=resulCita)

#----------------------------------------------------------Citas Registradas por Medico
@dentalShield.route("/DentalShield/citas-registradas-medicos")
@login_required
def viewcitasmedicos():
    idusuario = current_user.id
    print(idusuario)
    printdoctor = db.session.query(RegistroCita, Empleado, Servicio, Consultorio, Clinica 
    ).filter(
    RegistroCita.idEmpleRegis == Empleado.id,
    RegistroCita.idServicioRegis == Servicio.id,
    RegistroCita.idConsultorioReg == Consultorio.id,
    RegistroCita.idClinicaRegis == Clinica.id,
    RegistroCita.idEmpleRegis == idusuario).all()
    
    return render_template("clinica/vistaCitasMedicos.html", user=current_user, printdoctor=printdoctor)

#-------------------------------------------------------------Pagos Registrados 
@dentalShield.route("/DentalShield/pagos-registrados")
@login_required
def viewpagos():
    printPAgos = db.session.query(Pago, RegistroCita, Empleado, Servicio
        ).filter(
        Pago.idCitaPago == RegistroCita.id,
        Pago.idEmpleados == Empleado.id,
        RegistroCita.idServicioRegis == Servicio.id
        ).all()
    return render_template("clinica/vistapagos.html", user=current_user, printPAgos=printPAgos)


#------------------------------------------Actualizar Pagos
@dentalShield.route("/DentalShield/updatepagos/<int:id>", methods=["GET", "POST"])
@login_required
def updatepagos(id):
    upago =db.session.query(Pago).filter(Pago.id == id).first()

    if request.method == "POST":
        abono = request.form.get("abono")
        debe = upago.debe - float(abono)
        notaPago = request.form.get("notaPago")
        print(debe)
        print(upago.pagoTotal)

        error = None
        if not abono:
            error = "Se requiere ingresar una cantidad"
        elif not notaPago:
            error = "Se requiere un estatus del pago"

        if error is not None:
            flash(error)
        else:
            upago.abono = upago.pagoTotal - debe
            upago.debe = debe
            upago.notaPago = notaPago


            db.session.add(upago)
            db.session.commit()
            return redirect(url_for("DentalShield.viewpagos"))

    return render_template("clinica/pagos.html", user=current_user, upago=upago)


@dentalShield.route('/DentalShield/desc-pdf-ultima-cita')
def pdf_ultimacita():
    try:
        connection = pymysql.Connection(host="localhost", user="root", password="Donitas342", db="clinica_dental")
        cursorr = connection.cursor()
        cursorr.execute('SELECT * FROM registroCitas WHERE id = (SELECT MAX(id) FROM registroCitas);')
        lastid = cursorr.fetchall()
        last = lastid
        lista_datos = list(last)

        con = pymysql.connect(host='localhost', user='root', password='Donitas342', db='clinica_dental',cursorclass=pymysql.cursors.DictCursor)
        cursorrr = con.cursor()
        # cursorrr.execute("SELECT id, nombrePaciente, edad, telefono, nota, fechaRegistro, estatus, fechaCancelacion FROM registroCitas")
        cursorrr.execute("SELECT id, nombrePaciente, edad, telefono, nota, fechaRegistro, estatus, fechaCancelacion FROM registroCitas LIMIT 1")
        result = cursorrr.fetchall()

        # Create instance of FPDF class
        pdf = FPDF(orientation='L', unit='mm', format='A3')
        # Add new page. Without this you cannot create the document.
        pdf.add_page()

        # Set up a logo
        pdf.image('https://res.cloudinary.com/dzal2zrbb/image/upload/v1638171953/samples/bubbles/logo1_hmsfsf.png', x= 14, y=15.5, w=33, h=0, type='', link='')

        # Encabezado
        pdf.set_font('Times', 'B', 16.0)
        pdf.cell(w=0, h=20, txt='Mi Cita', border=1, align='C', fill=0, ln=1)
        pdf.ln(5)
        pdf.set_font('Arial', '', 9)

        # Columnas
        for row in result:
            # print(row)
            # print(type(row))
            dicColum = row.keys()
            listColum = list(dicColum)
            print(listColum)
            print(len(listColum))
            pdf.set_fill_color(193, 229, 252)  # Background colorof header
            pdf.cell(10, 12, str(listColum[0]), border=1, align='C', fill=1)
            pdf.cell(50, 12, str(listColum[1]), border=1, align='C', fill=1)
            pdf.cell(20, 12, str(listColum[2]), border=1, align='C', fill=1)
            pdf.cell(25, 12, str(listColum[3]), border=1, align='C', fill=1)
            pdf.cell(40, 12, str(listColum[4]), border=1, align='C', fill=1)
            pdf.cell(35, 12, str(listColum[5]), border=1, align='C', fill=1)
            pdf.cell(25, 12, str(listColum[6]), border=1, align='C', fill=1)
            pdf.multi_cell(w=0, h=12, txt=str(listColum[7]), border=1, align='L', fill=1)

        # Valores
        for row in lista_datos:
            pdf.cell(w=10, h=12, txt=str(row[0]), border=1, align='C', fill=0)
            pdf.cell(w=50, h=12, txt=str(row[1]), border=1, align='C', fill=0)
            pdf.cell(w=20, h=12, txt=str(row[2]), border=1, align='C', fill=0)
            pdf.cell(w=25, h=12, txt=str(row[3]), border=1, align='C', fill=0)
            pdf.cell(w=40, h=12, txt=str(row[4]), border=1, align='C', fill=0)
            pdf.cell(w=35, h=12, txt=str(row[5]), border=1, align='C', fill=0)
            pdf.cell(w=25, h=12, txt=str(row[6]), border=1, align='C', fill=0)
            pdf.multi_cell(w=0, h=12, txt=str(row[7]), border=1, align='L', fill=0)
            pdf.ln()

        # Set up a image
        pdf.image('https://res.cloudinary.com/dzal2zrbb/image/upload/v1638355218/samples/bubbles/banner_dentalShield_xcjhj2.png', x = 160, y =70, w = 90, h = 20, type = '', link = '')

        # Pie de pagina
        # Setting position at 1.5 cm from bottom:
        pdf.set_y(263)
        # Setting font: helvetica italic 8
        pdf.set_font("helvetica", "I", 8)
        # Setting text color to gray:
        pdf.set_text_color(128)
        # Printing page number
        pdf.cell(0, 10, f"Page {pdf.page_no()}", 0, 0, "C")

        pdf.output('ultima-cita.pdf', 'F')

        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',headers={'Content-Disposition': 'attachment;filename=ultima-cita.pdf'})

    except Exception as e:
        print(e)

    finally:
        print("Listo 🥵")

@dentalShield.route('/DentalShield/desc-pdf-citas-totales')
def pdf_citastotales():
    try:
        resulCita = db.session.query(RegistroCita, Empleado, Servicio, Consultorio, Clinica).filter(
            RegistroCita.idEmpleRegis == Empleado.id,
            RegistroCita.idServicioRegis == Servicio.id,
            RegistroCita.idConsultorioReg == Consultorio.id,
            RegistroCita.idClinicaRegis == Clinica.id).all()

        # Create instance of FPDF class
        pdf = FPDF(orientation='L', unit='mm', format='A3')
        # Add new page. Without this you cannot create the document.
        pdf.add_page()

        # Set up a logo
        pdf.image('https://res.cloudinary.com/dzal2zrbb/image/upload/v1638171953/samples/bubbles/logo1_hmsfsf.png', x= 14, y=15.5, w=33, h=0, type='', link='')

        # Encabezado
        pdf.set_font('Times', 'B', 16.0)
        pdf.cell(w=0, h=20, txt='Citas', border=1, align='C', fill=0, ln=1)
        pdf.ln(5)
        pdf.set_font('Arial', '', 9)

        # Columnas
        pdf.set_fill_color(193, 229, 252) #Background colorof header
        pdf.cell(w=10, h=12, txt='ID', border=1, align='C', fill=1)
        pdf.cell(w=50, h=12, txt='Nombre', border=1, align='C', fill=1)
        pdf.cell(w=15, h=12, txt='Edad', border=1, align='C', fill=1)
        pdf.cell(w=25, h=12, txt='Telefono', border=1, align='C', fill=1)
        pdf.cell(w=40, h=12, txt='Nota', border=1, align='C', fill=1)
        pdf.cell(w=35, h=12, txt='Fecha Registro', border=1, align='C', fill=1)
        pdf.cell(w=25, h=12, txt='Estatus', border=1, align='C', fill=1)
        pdf.cell(w=35, h=12, txt='Fecha Cancelación', border=1, align='C', fill=1)
        pdf.cell(w=35, h=12, txt='Servicio', border=1, align='C', fill=1)
        pdf.cell(w=20, h=12, txt='Total', border=1, align='C', fill=1)
        pdf.cell(w=25, h=12, txt='Clinica', border=1, align='C', fill=1)
        pdf.cell(w=20, h=12, txt='Consultorio', border=1, align='C', fill=1)
        pdf.multi_cell(w=0, h=12, txt='Empleado', border=1, align='C', fill=1)

        # Valores
        for valor in resulCita:
            ncompleto = valor.RegistroCita.nombrePaciente + " " + valor.RegistroCita.apellidoPatPaciente + " " + valor.RegistroCita.apellidoMatPaciente
            emcompleato = valor.Empleado.username + " " + valor.Empleado.apellidoPAtEmpleado + " " + valor.Empleado.apellidoMatEmpleado
            pdf.cell(w=10, h=12, txt=str(valor.RegistroCita.id), border=1, align='C', fill=0)
            pdf.cell(w=50, h=12, txt=ncompleto, border=1, align='L', fill=0)
            pdf.cell(w=15, h=12, txt=str(valor.RegistroCita.edad), border=1, align='C', fill=0)
            pdf.cell(w=25, h=12, txt=str(valor.RegistroCita.telefono), border=1, align='L', fill=0)
            pdf.cell(w=40, h=12, txt=valor.RegistroCita.nota, border=1, align='L', fill=0)
            pdf.cell(w=35, h=12, txt=str(valor.RegistroCita.fechaRegistro), border=1, align='C', fill=0)
            pdf.cell(w=25, h=12, txt=valor.RegistroCita.estatus, border=1, align='L', fill=0)
            pdf.cell(w=35, h=12, txt=str(valor.RegistroCita.fechaCancelacion), border=1, align='L', fill=0)
            pdf.cell(w=35, h=12, txt=valor.Servicio.nombreServicio, border=1, align='L', fill=0)
            pdf.cell(w=20, h=12, txt=str(valor.Servicio.costoServicio), border=1, align='C', fill=0)
            pdf.cell(w=25, h=12, txt=valor.Clinica.nombreClinica, border=1, align='L', fill=0)
            pdf.cell(w=20, h=12, txt=str(valor.Consultorio.id), border=1, align='C', fill=0)
            pdf.multi_cell(w=0, h=12, txt=emcompleato, border=1, align='L', fill=0)

        # Set up a image
        pdf.image('https://res.cloudinary.com/dzal2zrbb/image/upload/v1638355218/samples/bubbles/banner_dentalShield_xcjhj2.png', x = 160, y =70, w = 90, h = 20, type = '', link = '')

        # Pie de pagina
        # Setting position at 1.5 cm from bottom:
        pdf.set_y(263)
        # Setting font: helvetica italic 8
        pdf.set_font("helvetica", "I", 8)
        # Setting text color to gray:
        pdf.set_text_color(128)
        # Printing page number
        pdf.cell(0, 10, f"Page {pdf.page_no()}", 0, 0, "C")

        #pdf.output('citas-totales.pdf')
        #pdf.output('D','citas-totales.pdf')
        #pdf.output('citas-totales.pdf','D', True)
        #pdf.output('D','citas-totales.pdf', True)

        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',headers={'Content-Disposition': 'attachment;filename=citas-totales.pdf'})

    except Exception as e:
        print(e)

    finally:
        print("Listo 🥵")