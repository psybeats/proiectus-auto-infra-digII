import pymysql
mydb = pymysql.Connection( host="localhost", user="root", password="root", database="clinica_dental")
mycursor = mydb.cursor()

#Sacar promedio
def promedio():
  mycursor.execute("SELECT idEmpleRegis, username, apellidoPAtEmpleado, apellidoMatEmpleado, \
      round(sum(pagoTotalCitas),1) AS Total,  \
      round(avg(pagoTotalCitas),1) AS Promedio \
  FROM registroCitas \
  INNER JOIN empleados ON registroCitas.idEmpleRegis = empleados.id \
  GROUP BY idEmpleRegis \
  ORDER BY Total ASC;")
  promedio = mycursor.fetchall()
  #print(promedio[1][0])
  #print(promedio[1][1])
  #print(promedio[1][2])
  return(promedio)

#Consultar cuantas citas tuvo un medico
def citasMedico(nempleado):
  mycursor.execute("SELECT COUNT(registroCitas.id) as 'Citas Por Medico', username, apellidoPAtEmpleado, apellidoMatEmpleado \
  FROM registroCitas \
  INNER JOIN empleados ON registroCitas.idEmpleRegis = empleados.id \
  WHERE idEmpleRegis = %s;", (nempleado))
  contador = mycursor.fetchall()
  return(contador)

#Consultar cuantas citas tuvo un medico
def fechaxmedico(fecha,idempleado):

  mycursor.execute("SELECT registroCitas.id, nombrePaciente, apellidoPatPaciente, apellidoMatPaciente, \
    registroCitas.edad, registroCitas.telefono, nota, pagoTotalCitas, fechaRegistro, estatus, fechaCancelacion, \
  nombreServicio, pagoTotalCitas, nombreClinica, consultorios.id, \
  username, apellidoPAtEmpleado, apellidoMatEmpleado \
  FROM registroCitas \
  INNER JOIN empleados ON registroCitas.idEmpleRegis = empleados.id \
  INNER JOIN servicios ON registroCitas.idServicioRegis = servicios.id \
  INNER JOIN consultorios ON registroCitas.idConsultorioReg = consultorios.id \
  INNER JOIN clinicas ON registroCitas.idClinicaRegis = clinicas.id \
  WHERE DATE(fechaRegistro) = %s \
  AND empleados.id = %s;", (fecha, idempleado))
  fecha = mycursor.fetchall()
  return(fecha)