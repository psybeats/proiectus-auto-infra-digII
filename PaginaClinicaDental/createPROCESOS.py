import pymysql
import random

def random_registroCitas(idClinicaRegis):
  connection = pymysql.Connection(host="localhost", user="root", password="root", db="clinica_dental")
  cursorr = connection.cursor()

  cursorr.execute('SELECT empleados.id FROM empleados \
    WHERE idRolEmpleado = 2 AND idClinicaEmpleado = %s;', (idClinicaRegis))
  pemple = cursorr.fetchall()

  #Ordenar el resultado de fetchall ((1), (2))  para que salga en lista [1,2]
  fresult = [i[0] for i in pemple]
  print(fresult)
  # utilizando random.choice() para obtener un número aleatorio 
  # probeniente de la lista anteriormente creada 
  random_num = random.choice(fresult)
  print()
  cursorr.execute('SELECT idConsultorioEmple FROM empleados WHERE empleados.id = %s;', (random_num))
  consultorio = cursorr.fetchone()
  numero_consultorio = consultorio[0]
  
  pid = cursorr.execute('SELECT * FROM registroCitas;')
 
  cursorr.callproc('Insert_Emple_Random', [random_num,numero_consultorio,pid])


  connection.commit()
  connection.close()
  cursorr.close()

def crear_pagos():
  mydb = pymysql.Connection( host="localhost", user="root", password="root", database="clinica_dental")
  mycursor = mydb.cursor()

  mycursor.execute('SELECT MAX(id) AS id FROM registroCitas')
  lastid = mycursor.fetchone()
  last = lastid[0]

  s1 = ('SELECT costoServicio, registroCitas.id, idEmpleRegis FROM registroCitas \
    INNER JOIN servicios ON registroCitas.idServicioRegis = servicios.id WHERE registroCitas.id = %s')

  s2 = ('SELECT registroCitas.id, costoServicio FROM registroCitas \
    INNER JOIN servicios ON registroCitas.idServicioRegisDos = servicios.id WHERE registroCitas.id = %s')

  s3 = ('SELECT registroCitas.id,costoServicio FROM registroCitas \
    INNER JOIN servicios ON registroCitas.idServicioRegisTres = servicios.id WHERE registroCitas.id = %s')
  mycursor.execute(s1, (last,))
  myresult = mycursor.fetchall()


  mycursor.execute(s2, (last,))
  myresult2 = mycursor.fetchone()
  mycursor.execute(s3, (last,))
  myresult3 = mycursor.fetchone()
  costo1 = myresult2[1]
  costo2 = myresult3[1]

  print(myresult2[1])
  print(myresult3[1])

  totalRegUno = myresult[0][0]
  total = totalRegUno + costo1 + costo2
  pagostado = "Por Pagar"
  abono = 0.0
  deuda = total
  idcita = myresult[0][1]
  idempleado = myresult[0][2]

  mycursor.callproc('insert_pago', (total, abono, deuda, pagostado, idcita, idempleado))
  mycursor.callproc('pago_update', (total, last))

  mydb.commit()
  mydb.close()
  mycursor.close()