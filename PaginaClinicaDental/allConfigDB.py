import pymysql


def insertar_datos():
    try:
        # Inicializa la conexión utilizando una DB previamente creada.
        connection = pymysql.Connection(host="localhost", user="root", password="root", db="clinica_dental")
        cursorr = connection.cursor()
        sql01 = "INSERT INTO `consultorios` (`id`, `horario`) VALUES (%s, %s)"
        sql02 = "INSERT INTO `consultorios` (`id`, `horario`) VALUES (%s, %s)"
        cursorr.execute(sql01, (0o1, "Matutino"))
        cursorr.execute(sql02, (0o2, "Vespertino"))
        sql03 = "INSERT INTO `clinicas` (`id`, `nombreClinica`, `direcccion`, `telefono`) VALUES (%s, %s, %s, %s)"
        sql04 = "INSERT INTO `clinicas` (`id`, `nombreClinica`, `direcccion`, `telefono`) VALUES (%s, %s, %s, %s)"
        sql05 = "INSERT INTO `clinicas` (`id`, `nombreClinica`, `direcccion`, `telefono`) VALUES (%s, %s, %s, %s)"
        cursorr.execute(sql03, (0o1, "Dental Shield", "Emiliano Zapata #1", "7351234567"))
        cursorr.execute(sql04, (0o2, "Dental Shield 2", "Emiliano Zapata #2", "7353456739"))
        cursorr.execute(sql05, (0o3, "Dental Shield 3", "Emiliano Zapata #10", "7359575739"))
        sql06 = "INSERT INTO `roles` (`id`, `tipoRol`) VALUES (%s, %s)"
        sql07 = "INSERT INTO `roles` (`id`, `tipoRol`) VALUES (%s, %s)"
        sql08 = "INSERT INTO `roles` (`id`, `tipoRol`) VALUES (%s, %s)"
        cursorr.execute(sql06, (0o1, "Administrador"))
        cursorr.execute(sql07, (0o2, "Medico"))
        cursorr.execute(sql08, (0o3, "Asistente administrativo"))
        sql09 = "INSERT INTO `servicios` (`id`, `nombreServicio`, `costoServicio`) VALUES (%s, %s, %s)"
        sql10 = "INSERT INTO `servicios` (`id`, `nombreServicio`, `costoServicio`) VALUES (%s, %s, %s)"
        sql11 = "INSERT INTO `servicios` (`id`, `nombreServicio`, `costoServicio`) VALUES (%s, %s, %s)"
        sql12 = "INSERT INTO `servicios` (`id`, `nombreServicio`, `costoServicio`) VALUES (%s, %s, %s)"
        sql13 = "INSERT INTO `servicios` (`id`, `nombreServicio`, `costoServicio`) VALUES (%s, %s, %s)"
        sql14 = "INSERT INTO `servicios` (`id`, `nombreServicio`, `costoServicio`) VALUES (%s, %s, %s)"
        sql15 = "INSERT INTO `servicios` (`id`, `nombreServicio`, `costoServicio`) VALUES (%s, %s, %s)"
        sql16 = "INSERT INTO `servicios` (`id`, `nombreServicio`, `costoServicio`) VALUES (%s, %s, %s)"
        sql17 = "INSERT INTO `servicios` (`id`, `nombreServicio`, `costoServicio`) VALUES (%s, %s, %s)"
        cursorr.execute(sql09, (0o1, "Sin Servicio Registrado", 00))
        cursorr.execute(sql09, (0o2, "Revisión General", 300))
        cursorr.execute(sql10, (0o3, "Cirugía Oral", 2500))
        cursorr.execute(sql11, (0o4, "Odontología Preventiva", 1800))
        cursorr.execute(sql12, (0o5, "Endodoncia", 2500))
        cursorr.execute(sql13, (0o6, "Prótesis Dental", 1900))
        cursorr.execute(sql14, (0o7, "Odontología infantil", 1300))
        cursorr.execute(sql15, (0o10, "Limpieza Dental", 500))
        cursorr.execute(sql16, (0o11, "Extracción de Muela", 600))
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
        connection = pymysql.Connection(host="localhost", user="root", password="root", db="clinica_dental")
        cursorr = connection.cursor()
        sql = "INSERT INTO `empleados` (`id`, `username`, `apellidoPAtEmpleado`, `apellidoMatEmpleado`, `password`, `correoElectronico`, `estadoEmpleado`, `creado`, `idConsultorioEmple`, `idClinicaEmpleado`, `idRolEmpleado`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursorr.execute(sql, (0o1, "Administrador", "Dental", "Shield", 'sha256$BOl2pwcjY6kKSgCi$25b90dc07cfc3099088d58222a05544ee896904dbff68c962942beab4e23f8c8', "admin@DentalShield@gmail.com", "Activo", "2021-11-18 22:24:41", 0o1, 0o1, 0o1))
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