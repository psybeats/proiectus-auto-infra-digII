import pymysql


def random_registroCitas():
  connection = pymysql.Connection(host="localhost", user="root", password="root", db="clinica_dental")
  cursorr = connection.cursor()

  pemple = cursorr.execute('SELECT * FROM empleados WHERE idRolEmpleado = 2;')
  pconsul = cursorr.execute('SELECT * FROM consultorios;')
  pid = cursorr.execute('SELECT * FROM registroCitas;')
 
  cursorr.callproc('Insert_Emple_Consul_Random1', [pemple,pconsul,pid])


  connection.commit()
  connection.close()
  cursorr.close()

def crear_pagos():
  mydb = pymysql.Connection(
  host="localhost",
  user="root",
  password="root",
  database="clinica_dental"
  )
  mycursor = mydb.cursor()

  mycursor.execute('SELECT MAX(id) AS id FROM registroCitas')
  lastid = mycursor.fetchone()
  last = lastid[0]

  s1 = ('SELECT costoServicio, registroCitas.id, idEmpleRegis FROM registroCitas INNER JOIN servicios ON registroCitas.idServicioRegis = servicios.id WHERE registroCitas.id = %s')
  mycursor.execute(s1, (last,))
  myresult = mycursor.fetchall()
  total = myresult[0][0]
  pagostado = "Por Pagar"
  abono = 0.0
  deuda = total
  idcita = myresult[0][1]
  idempleado = myresult[0][2]


  print(last)
  print()
  print(total)
  print(pagostado)
  print(abono)
  print(deuda)
  print(idcita)
  print(idempleado)
  print()

  mycursor.callproc('insert_pago', (total, abono, deuda, pagostado, idcita, idempleado))

  mydb.commit()
  mydb.close()
  mycursor.close()