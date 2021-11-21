import pymysql


def random_registoCitas():
  connection = pymysql.Connection(host="localhost", user="root", password="root", db="clinica_dental")
  cursorr = connection.cursor()

  pemple = cursorr.execute('SELECT * FROM empleados WHERE idRolEmpleado = 2;')
  pconsul = cursorr.execute('SELECT * FROM consultorios;')
  pid = cursorr.execute('SELECT * FROM registroCitas;')
  print(pemple)
  print(pconsul)
  print(pid)
 
  cursorr.callproc('Insert_Emple_Consul_Random', [pemple,pconsul,pid])


  connection.commit()
  connection.close()
  cursorr.close()




