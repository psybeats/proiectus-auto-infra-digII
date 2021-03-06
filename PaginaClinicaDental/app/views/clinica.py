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
import functions as f

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

# Ver Servicios
def viewservicios():
    servicios = db.session.query(Servicio).filter(Servicio.id >= 2).all()
    flash(MENSAJE, category='success')
    return render_template("clinica/serviciosC.html", user=current_user, servicios=servicios)

#Registro de Citas
@dentalShield.route("/DentalShield/citas", methods=["GET", "POST"])
def citas():
    posts = db.session.query(Servicio).filter(Servicio.id >= 2).all() 
    servTo = Servicio.query.all()
    clinica = Clinica.query.all()
   
    if request.method == "POST":
        nombrePaciente = request.form.get("nombrePaciente")
        apellidoPatPaciente = request.form.get("apellidoPatPaciente")
        apellidoMatPaciente = request.form.get("apellidoMatPaciente")
        edad = request.form.get("edad")
        estatus = "Cita Activa"
        telefono = request.form.get("telefono")
        nota = "Sin Nota Previa"
        fecha = request.form.get("fecha")
        hora = request.form.get("hora")
        fechaCancelacion = request.form.get("fechaCancelacion") 
        idServicioRegis = request.form.get("nombreServicio")
        idServicioRegisDos = request.form.get("nombreServicio2")
        idServicioRegisTres =  request.form.get("nombreServicio3")
        idClinicaRegis = request.form.get("idClinicaRegis")
        
        fechaRegistro = fecha + " " + hora

        registro = RegistroCita(nombrePaciente, apellidoPatPaciente, apellidoMatPaciente, edad, estatus, telefono, nota, fechaRegistro, fechaCancelacion, idServicioRegis, idServicioRegisDos, idServicioRegisTres, idClinicaRegis)

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
            error = "Se requiere el tel??fono del paciente"
        elif not fechaRegistro:
            error = "Se requiere una fecha de registro"

        if error is not None:
            flash(error)
        else:
            
            db.session.add(registro)
            db.session.commit()

            #CAUSA FALLAS, SOLUCIONAR!
            p.random_registroCitas(idClinicaRegis)
            p.crear_pagos()
            
            return redirect(url_for("DentalShield.printCitas"))

    return render_template("clinica/citas.html", posts=posts, clinica=clinica, user=current_user, servTo=servTo)

#Print Vista Citas
@dentalShield.route("/DentalShield/printCitas")
def printCitas():
    mydb = pymysql.Connection(host="localhost", user="root", password="root", database="clinica_dental")
    mycursor = mydb.cursor()

    mycursor.execute('SELECT MAX(id) AS id FROM registroCitas')
    lastid = mycursor.fetchone()
    idFin = lastid[0]

    ultimoReg = db.session.query(RegistroCita, Empleado, Servicio, Consultorio, Clinica 
    ).filter(
    RegistroCita.idEmpleRegis == Empleado.id,
    RegistroCita.idServicioRegis == Servicio.id,
    RegistroCita.idConsultorioReg == Consultorio.id,
    RegistroCita.idClinicaRegis == Clinica.id,
    RegistroCita.id == idFin).all()


    s2 = ('SELECT registroCitas.id, nombreServicio FROM registroCitas \
    INNER JOIN servicios ON registroCitas.idServicioRegisDos = servicios.id WHERE registroCitas.id = %s')

    s3 = ('SELECT registroCitas.id, nombreServicio FROM registroCitas \
    INNER JOIN servicios ON registroCitas.idServicioRegisTres = servicios.id WHERE registroCitas.id = %s')

    mycursor.execute(s2, (idFin,))
    servicio1 = mycursor.fetchone()

    mycursor.execute(s3, (idFin,))
    servicio2 = mycursor.fetchone()

    return render_template("clinica/printCitas.html", user=current_user, ultimoReg=ultimoReg, servicio1=servicio1, servicio2=servicio2 )


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
    ucita = db.session.query(RegistroCita).filter(RegistroCita.id == id).first()
    
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
            error = "Se requiere el tel??fono del paciente"
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

#---------------------------- Citas Registradas por Busqueda
@dentalShield.route("/DentalShield/busqueda-citas-registras", methods=["GET", "POST"])
@login_required
def viewcitasxsearch():
    busquedas = ''
    prome = ''
    if request.method == "POST":
        fecha1 = request.form.get('primerFecha')
        fecha2 = request.form.get('segundaFecha')

        busquedas = db.session.query(RegistroCita, Empleado, Servicio, Consultorio, Clinica 
        ).filter(
        RegistroCita.idEmpleRegis == Empleado.id,
        RegistroCita.idServicioRegis == Servicio.id,
        RegistroCita.idConsultorioReg == Consultorio.id,
        RegistroCita.idClinicaRegis == Clinica.id,
        RegistroCita.fechaRegistro.between(fecha1,fecha2)).all()

        prome = f.promedio()
        print(prome)

    return render_template("clinica/vistaCitasBusca.html", user=current_user, busquedas=busquedas, prome=prome)

#---------------------------------------------------------Ver Citas, por medico y por fecha 
@dentalShield.route("/DentalShield/citas-registradas-date", methods=["GET", "POST"])
@login_required
def viewcitasdatemedic():
    empleado = db.session.query(Empleado).filter(Empleado.idRolEmpleado == 2).all()
    buscarDE = ''
    totalCitas = ''
    fecha = ''
    if request.method == "POST":
        fecha = request.form.get('fecha')
        nempleado = request.form.get('idempleado')

        buscarDE = f.fechaxmedico(fecha,nempleado)
        totalCitas = f.citasMedico(nempleado)
        
    return render_template("clinica/vistaCitasDateMed.html", user=current_user, empleado=empleado, buscarDE=buscarDE, totalCitas=totalCitas, fecha=fecha)
    
#----------------------------------------------------------Citas Registradas por Medico
@dentalShield.route("/DentalShield/citas-registradas-medicos")
@login_required
def viewcitasmedicos():
    idusuario = current_user.id
    #print(idusuario)
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
        #print(debe)
        #print(upago.pagoTotal)

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
        connection = pymysql.Connection(host="localhost", user="root", password="root", db="clinica_dental")
        cursorr = connection.cursor()
        cursorr.execute('SELECT registroCitas.id FROM registroCitas WHERE id = (SELECT MAX(id) FROM registroCitas);')
        lastid = cursorr.fetchone()
        last = lastid[0]
        print(last)


        unaCita = db.session.query(RegistroCita, Empleado, Servicio, Consultorio, Clinica 
        ).filter(
        RegistroCita.idEmpleRegis == Empleado.id,
        RegistroCita.idServicioRegis == Servicio.id,
        RegistroCita.idConsultorioReg == Consultorio.id,
        RegistroCita.idClinicaRegis == Clinica.id
        ).filter(RegistroCita.id == last).all()

        # Create instance of FPDF class
        pdf = FPDF(orientation='L', unit='mm', format='A3')
        # Add new page. Without this you cannot create the document.
        pdf.add_page()

        # Set up a logo
        pdf.image('https://res.cloudinary.com/dzal2zrbb/image/upload/v1638171953/samples/bubbles/logo1_hmsfsf.png', x= 14, y=15.5, w=33, h=0, type='', link='')

        # Encabezado
        pdf.set_font('Times', 'B', 16.0)
        pdf.cell(w=0, h=20, txt='Registro de Cita', border=1, align='C', fill=0, ln=1)
        pdf.ln(5)
        pdf.set_font('Arial', '', 10)

        # Columnas
        #for row in result:
            # print(type(row))
        #   dicColum = row.keys()
        #    listColum = list(dicColum)
        #    print(listColum)
        #    print(len(listColum))
        pdf.set_fill_color(193, 229, 252)  # Background colorof header

        # Valores

        for valor in unaCita:
            ncompleto = valor.RegistroCita.nombrePaciente + " " + valor.RegistroCita.apellidoPatPaciente + " " + valor.RegistroCita.apellidoMatPaciente
            emcompleato = valor.Empleado.username + " " + valor.Empleado.apellidoPAtEmpleado + " " + valor.Empleado.apellidoMatEmpleado

            pdf.cell(w=170, h=12, txt="", border=0, align='C', fill=0)
            pdf.cell(w=45, h=12, txt='ID: ', border=0, align='L', fill=0)
            pdf.multi_cell(w=10, h=12, txt=str(valor.RegistroCita.id), border=0, align='C', fill=0)
            pdf.cell(w=170, h=12, txt="", border=0, align='C', fill=0)
            pdf.cell(w=45, h=12, txt='Nombre: ', border=0, align='L', fill=0)
            pdf.multi_cell(w=50, h=12, txt=ncompleto, border=0, align='L', fill=0)
            pdf.cell(w=170, h=12, txt="", border=0, align='C', fill=0)
            pdf.cell(w=45, h=12, txt='Edad: ', border=0, align='L', fill=0)
            pdf.multi_cell(w=15, h=12, txt=str(valor.RegistroCita.edad), border=0, align='L', fill=0)
            pdf.cell(w=170, h=12, txt="", border=0, align='C', fill=0)
            pdf.cell(w=45, h=12, txt='Telefono: ', border=0, align='L', fill=0)
            pdf.multi_cell(w=30, h=12, txt=str(valor.RegistroCita.telefono), border=0, align='L', fill=0)
            pdf.cell(w=170, h=12, txt="", border=0, align='C', fill=0)
            pdf.cell(w=45, h=12, txt='Nota: ', border=0, align='L', fill=0)
            pdf.multi_cell(w=40, h=12, txt=valor.RegistroCita.nota, border=0, align='L', fill=0)
            pdf.cell(w=170, h=12, txt="", border=0, align='C', fill=0)
            pdf.cell(w=45, h=12, txt='Fecha Registro: ', border=0, align='L', fill=0)
            pdf.multi_cell(w=45, h=12, txt=str(valor.RegistroCita.fechaRegistro), border=0, align='L', fill=0)
            pdf.cell(w=170, h=12, txt="", border=0, align='C', fill=0)
            pdf.cell(w=45, h=12, txt='Estatus: ', border=0, align='L', fill=0)
            pdf.multi_cell(w=25, h=12, txt=valor.RegistroCita.estatus, border=0, align='L', fill=0)
            pdf.cell(w=170, h=12, txt="", border=0, align='C', fill=0)
            pdf.cell(w=45, h=12, txt='Servicio: ', border=0, align='L', fill=0)
            pdf.multi_cell(w=35, h=12, txt=valor.Servicio.nombreServicio, border=0, align='L', fill=0)
            pdf.cell(w=170, h=12, txt="", border=0, align='C', fill=0)
            pdf.cell(w=45, h=12, txt='Total: ', border=0, align='L', fill=0)
            pdf.multi_cell(w=20, h=12, txt=str(valor.Servicio.costoServicio), border=0, align='L', fill=0)
            pdf.cell(w=170, h=12, txt="", border=0, align='C', fill=0)
            pdf.cell(w=45, h=12, txt='Clinica: ', border=0, align='L', fill=0)
            pdf.multi_cell(w=35, h=12, txt=valor.Clinica.nombreClinica, border=0, align='L', fill=0)
            pdf.cell(w=170, h=12, txt="", border=0, align='C', fill=0)
            pdf.cell(w=45, h=12, txt='Consultorio: ', border=0, align='L', fill=0)
            pdf.multi_cell(w=20, h=12, txt=str(valor.Consultorio.id), border=0, align='L', fill=0)
            pdf.cell(w=170, h=12, txt="", border=0, align='C', fill=0)
            pdf.cell(w=45, h=12, txt='Empleado: ', border=0, align='L', fill=0)
            pdf.multi_cell(w=45, h=12, txt=emcompleato, border=0, align='L', fill=0)
            pdf.cell(w=170, h=12, txt="", border=0, align='C', fill=0)
            #pdf.ln()

        pdf.multi_cell(w=10, h=10, txt="", border=0, align='C', fill=0)
        pdf.multi_cell(w=0, h=10, txt="Apreciado " + ncompleto + ":", border=1, align='C', fill=0)
        pdf.multi_cell(w=0, h=10, txt="??Gracias por preferirnos! Estamos contentos de que haya\
            solicitado un servicio con nosotros. Nuestro objetivo es que siempre est?? satisfecho,\
            as?? que av??senos si su nivel de satisfacci??n es el adecuado.", border=0, align='C', fill=0)
        pdf.multi_cell(w=0, h=10, txt="??Lo estaremos esperando! ", border=0, align='C', fill=0)
        pdf.multi_cell(w=0, h=10, txt="??Que tengas un gran d??a!", border=0, align='C', fill=0)
        pdf.multi_cell(w=0, h=5, txt="", border=0, align='C', fill=0)
        pdf.multi_cell(w=0, h=10, txt="Atentamente, ", border=0, align='C', fill=0)
        pdf.multi_cell(w=0, h=10, txt="Tus amigos en DentalShield,", border=0, align='C', fill=0)

        # Set up a image
        #pdf.image('https://res.cloudinary.com/dzal2zrbb/image/upload/v1638355218/samples/bubbles/banner_dentalShield_xcjhj2.png', x = 160, y =70, w = 90, h = 20, type = '', link = '')

        # Pie de pagina
        # Setting position at 1.5 cm from bottom:
        pdf.set_y(263)
        # Setting font: helvetica italic 8
        pdf.set_font("helvetica", "I", 8)
        # Setting text color to gray:
        pdf.set_text_color(128)
        # Printing page number
        pdf.cell(0, 10, f"Page {pdf.page_no()}", 0, 0, "C")

        pdf.output('regisrto-cita.pdf', 'F')

        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',headers={'Content-Disposition': 'attachment;filename=registro-cita.pdf'})

    except Exception as e:
        print(e)

    finally:
        print("Listo ????")

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
        pdf.cell(w=35, h=12, txt='Fecha Cancelaci??n', border=1, align='C', fill=1)
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
            pdf.cell(w=20, h=12, txt=str(valor.RegistroCita.pagoTotalCitas), border=1, align='C', fill=0)
            pdf.cell(w=25, h=12, txt=valor.Clinica.nombreClinica, border=1, align='L', fill=0)
            pdf.cell(w=20, h=12, txt=str(valor.Consultorio.id), border=1, align='C', fill=0)
            pdf.multi_cell(w=0, h=12, txt=emcompleato, border=1, align='L', fill=0)

        # Set up a image
        #pdf.image('https://res.cloudinary.com/dzal2zrbb/image/upload/v1638355218/samples/bubbles/banner_dentalShield_xcjhj2.png', x = 160, y =70, w = 90, h = 20, type = '', link = '')

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
        print("Listo ????")


#Vista Empleados
@dentalShield.route("/DentalShield/Empleados")
@login_required
def viweempleados():
    ResulEmp = db.session.query(Empleado, Rol, Consultorio, Clinica 
    ).filter(Empleado.id == Empleado.id,
    Empleado.idRolEmpleado == Rol.id,
    Empleado.idConsultorioEmple == Consultorio.id,
    Empleado.idClinicaEmpleado == Clinica.id).all()
    return render_template("clinica/vistaempleados.html", user=current_user, ResulEmp=ResulEmp)