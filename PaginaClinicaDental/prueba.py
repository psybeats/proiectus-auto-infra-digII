import pymysql
import random

connection = pymysql.Connection(host="localhost", user="root", password="root", db="clinica_dental")
cursorr = connection.cursor()


cursorr.execute('SELECT id FROM empleados WHERE idRolEmpleado = 2;')
pemple = cursorr.fetchall()


#Ordenar el resultado de fetchall ((1), (2))  para que salga en lista [1,2]
fresult = [i[0] for i in pemple]
print(fresult)
print()

# Resultado de la lista 
print ("Original list is : " + str(fresult))
print()  

# utilizando random.choice() para obtener un número aleatorio 
# probeniente de la lista anteriormente creada 
random_num = random.choice(fresult)
print(random_num)