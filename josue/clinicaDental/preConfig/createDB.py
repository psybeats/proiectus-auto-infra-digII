import pymysql


def crear_db():
    try:
        # Inicializa la conexión utilizando una DB previamente creada (se trata de una DB preestablecida)
        connection = pymysql.Connection(host="localhost", user="root", password="qwerty123", db="mysql")
        cursorr = connection.cursor()
        # Se crea una nueva DB utilizando la conexión existente
        cursorr.execute("CREATE DATABASE IF NOT EXISTS clinica_dental")
        # Finaliza la conexión
        connection.close()
        cursorr.close()
        # Se crea una nueva conexión utilizando la DB creada anteriormente
        connection = pymysql.Connection(host="localhost", user="root", password="qwerty123", db="clinica_dental")
        cursorr = connection.cursor()
        # Crea la tabla tblestudiantes
        #cursorr.execute("CREATE TABLE IF NOT EXISTS empleados ( Id_Usuario INT(11) AUTO_INCREMENT, Nom_Usuario VARCHAR(30) NOT NULL, Ape_Usuario VARCHAR(30), Mat_Usuario VARCHAR(11) NOT NULL UNIQUE, Tel_Usuario VARCHAR(10) UNIQUE, Dir_Usuario VARCHAR(50),Email_Usuario VARCHAR(50) UNIQUE,Fec_Nac_Usuario DATE NOT NULL, Estado_Usuario VARCHAR(18), CONSTRAINT Usuario_pk PRIMARY KEY (Id_Usuario) )")
        cursorr.execute("SHOW DATABASES")
        connection.commit()
        connection.close()
        cursorr.close()
    except Exception as e:
        print(e)
    finally:
        print("\nÉxito🔥")


crear_db()
