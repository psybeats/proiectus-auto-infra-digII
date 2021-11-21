import pymysql

connection = pymysql.Connection(host="localhost", user="root", password="root", db="clinica_dental")
cursorr = connection.cursor()

pid = cursorr.execute('SELECT * FROM empleados where idRolEmpleado = 2')
print(pid)


connection.commit()
connection.close()
cursorr.close()