import pymysql

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

total1 = float(total)

deuda = total
idcita = myresult[0][1]
idempleado = myresult[0][2]
abono1= float(abono)
deuda1 = float(deuda)

print(last)
print()
print(total)
print(pagostado)
print(abono)
print(deuda)
print(idcita)
print(idempleado)
print()

mycursor.callproc('insert_pago', (2300, 0, 2300, "Por Pagar", 2, 1))

mydb.commit()
mydb.close()
mycursor.close()