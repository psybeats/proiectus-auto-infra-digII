import pymysql


def insertar_datos():
    try:
        # Inicializa la conexión utilizando una DB previamente creada.
        connection = pymysql.Connection(host="localhost", user="root", password="Donitas342", db="clinica_dental")
        cursorr = connection.cursor()
        sql01 = "INSERT INTO `consultorios` (`id`, `horario`) VALUES (%s, %s)"
        sql02 = "INSERT INTO `consultorios` (`id`, `horario`) VALUES (%s, %s)"
        cursorr.execute(sql01, (0o1, "Matutino"))
        cursorr.execute(sql02, (0o2, "Vespertino"))
        sql03 = "INSERT INTO `clinicas` (`id`, `nombreClinica`, `direcccion`, `telefono`) VALUES (%s, %s, %s, %s)"
        sql04 = "INSERT INTO `clinicas` (`id`, `nombreClinica`, `direcccion`, `telefono`) VALUES (%s, %s, %s, %s)"
        cursorr.execute(sql03, (0o1, "Dental Shield", "Emiliano Zapata #1", "7351234567"))
        cursorr.execute(sql04, (0o2, "Teeth's", "Emiliano Zapata #2", "7353456739"))
        sql05 = "INSERT INTO `roles` (`id`, `tipoRol`) VALUES (%s, %s)"
        sql06 = "INSERT INTO `roles` (`id`, `tipoRol`) VALUES (%s, %s)"
        sql07 = "INSERT INTO `roles` (`id`, `tipoRol`) VALUES (%s, %s)"
        cursorr.execute(sql05, (0o1, "Administrador"))
        cursorr.execute(sql06, (0o2, "Medico"))
        cursorr.execute(sql07, (0o3, "Asistente administrativo"))
        connection.commit()
        connection.close()
        cursorr.close()
    except Exception as e:
        print(e)
    finally:
        print("\nÉxito🔥")


def crear_usuario():
    try:
        # Inicializa la conexión utilizando una DB previamente creada.
        connection = pymysql.Connection(host="localhost", user="root", password="Donitas342", db="clinica_dental")
        cursorr = connection.cursor()
        sql = "INSERT INTO `empleados` (`id`, `username`, `apellidoPAtEmpleado`, `apellidoMatEmpleado`, `password`, `correoElectronico`, `estadoEmpleado`, `creado`, `idConsultorioEmple`, `idClinicaEmpleado`, `idRolEmpleado`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursorr.execute(sql, (0o1, "Administrador", "Dental", "Shield", 'sha256$BOl2pwcjY6kKSgCi$25b90dc07cfc3099088d58222a05544ee896904dbff68c962942beab4e23f8c8', "admin@witheteeth@gmail.com", "Activo", "2021-11-18 22:24:41", 0o1, 0o1, 0o1))
        #user:admin pass:qwerty
        connection.commit()
        connection.close()
        cursorr.close()
    except Exception as e:
        print(e)
    finally:
        print("\nÉxito🔥")


insertar_datos()
crear_usuario()
