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

from app import db

fecha1 = '2021-12-04'
fecha2 = '2021-12-05'

resulCita = db.session.query(RegistroCita, Empleado, Servicio, Consultorio, Clinica 
    ).filter(
    RegistroCita.idEmpleRegis == Empleado.id,
    RegistroCita.idServicioRegis == Servicio.id,
    RegistroCita.idConsultorioReg == Consultorio.id,
    RegistroCita.idClinicaRegis == Clinica.id
    ).filter(RegistroCita.fechaRegistro.between(fecha1,fecha2)).all()
print(resulCita)

