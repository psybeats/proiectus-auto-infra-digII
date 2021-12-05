from flask import Flask , Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from fpdf import FPDF
from sqlalchemy.orm import joinedload

from werkzeug.exceptions import abort
import pymysql
from flask_login import login_required, current_user
from app.mensajesflash import *

try:
    connection = pymysql.Connection(host="localhost", user="root", password="root", db="clinica_dental")
    cursorr = connection.cursor()
    cursorr.execute('SELECT * FROM registroCitas WHERE id = (SELECT MAX(id) FROM registroCitas);')
    lastid = cursorr.fetchall()
    last = lastid
    lista_datos = list(last)

    con = pymysql.connect(host='localhost', user='root', password='root', db='clinica_dental',cursorclass=pymysql.cursors.DictCursor)
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

    pdf.output('ultima-cita.pdf', 'F')
    Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',headers={'Content-Disposition': 'attachment;filename=registro-cita.pdf'})

except Exception as e:
    print(e)

finally:
    print("Listo 🥵")