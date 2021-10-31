#drop database clinicadental;
create database clinicaDental;
use clinicaDental;

create table clinicas(
idClinica int auto_increment,
nombreClinica varchar (255),
direcccion varchar (255),
telefono varchar (50),
constraint pk_ic primary key (idClinica)
);
insert into clinicas values (01, "Withe Teeth", "Emiliano Zapata #1", "7351234567");
insert into clinicas values (02, "Withe Teeth 2", "San Juan #29", "7351234567");
#delete from clinicas where idClinica = 05;
select * from clinicas;


create table servicios(
idServicio int auto_increment,
nombreServicio varchar (255),
costoServicio float,
constraint pk_is primary key (idServicio)
);
insert into servicios values (01, "Extraccion de Muela", 600);
insert into servicios values (02, "Cirugía Oral", 2500);
insert into servicios values (03, "Odontología Preventiva", 1800);
insert into servicios values (04, "Endodoncia", 2500);
insert into servicios values (05, "Protesis Dental", 1900);
insert into servicios values (06, "Odontología infantil", 1300);
insert into servicios values (07, "Limpieza Dental", 500);
select * from servicios;


create table roles (
idRol int auto_increment,
tipoRol varchar (50),
constraint pk_ir primary key (idRol)
);
insert into roles values (01, "Administrador");
insert into roles values (02, "Medico");
insert into roles values (03, "Asistente Administrativo");

create table consultorios(
claveC1 int auto_increment,
horario varchar (12),
constraint pk_icon primary key (claveC1)
);
insert into consultorios values (01, 'Matutino');
insert into consultorios values (02, 'Vespertino');


create table empleados(
idEmpleado int auto_increment,
nombreEmpleado varchar(255),
apellidoPAtEmpleado varchar(255),
apellidoMatEmpleado varchar(255),
cedulaProfesional varchar(255),
correoElectronico varchar(255),
contraseña varchar (50),
estadoEmpleado varchar (50),
idConsultorioEmple int,
idClinicaEmpleado int,
idRolEmpleado int,
constraint pk_ie primary key (idEmpleado),
constraint fk_cemp foreign key (idConsultorioEmple) references consultorios (claveC1), #01, 02
constraint fk_ice foreign key (idClinicaEmpleado) references clinicas (idClinica), #01
constraint fk_ire foreign key (idRolEmpleado) references roles (idRol) #01, 02, 03
);
insert into empleados values (01, "Arturo", "Flores", "Gomez", "SIN", "arturo@witheteeth@gmail.com", "arturo123", "Activo", 01, 01, 01);
insert into empleados values (02, "Alan", "Gutierrez", "Cortez", "01928381M", "alan@witheteeth@gmail.com", "alan123", "Activo", 02, 01, 02);
insert into empleados values (03, "Javier", "Bernal", "Flores", "SIN", "Javier@witheteeth@gmail.com", "javi123", "Activo", 02, 01, 01);
insert into empleados values (04, "Teodulfo", "Alegre", "Pineda", "01928482M", "teo@witheteeth@gmail.com", "teo123", "Activo", 02, 01, 02);
insert into empleados values (05, "Josue", "Vela", "Valle", "SIN", "josue@witheteeth@gmail.com", "josue123", "Activo", 01, 01, 01);
select * from empleados;

create table registroCitas (
idCitas int auto_increment,
nombrePaciente varchar (255),
apellidoPatPaciente varchar (255),
apellidoMatPaciente varchar (255),
edad int,
telefono varchar (50),
estado varchar(50),
costo float,
nota varchar (250),
fechaRegistro datetime DEFAULT(NOW()),
idServicioRegis int,
idClinicaRegis int,
idConsultorioReg int,
idEmpleRegis int,
constraint pk_irc primary key (idCitas),
constraint fk_is3 foreign key (idServicioRegis) references servicios (idServicio),
constraint fk_cr foreign key (idConsultorioReg) references consultorios (claveC1),
constraint fk_clre foreign key (idClinicaRegis) references clinicas (idClinica),
constraint fk_emr foreign key (idEmpleRegis) references empleados (idEmpleado)
);
insert into registroCitas values (01, "Jose", "Fernadez", "Perez", 23, "7251299920", "Cita Activa", 500, 
"El paciente cuenta con sangrado bucal", '2021-09-27 11:00:00', 01, 01, 02, 02);
insert into registroCitas values (02, "Alberto", "Herrera", "Cortez", 25, "7351828810", "Cita Activa", 2000,
"El paciente presenta problemas cardiacos", '2021-09-27 12:00:00', 04, 01, 01, 04);
insert into registroCitas values (03, "Ramon", "Zapata", "Sanchez", 30, "7778129300", "Cita Cancelada", 1800,
"El paciente es alergico a la penicilina", '2021-09-29 15:33:00',  03, 01, 01, 04);
insert into registroCitas values (04, "Cesar", "Soto", "Zapata", 23, "7771829381", "Cita Activa", 1200,
"El paciente cuenta con diabetes", '2021-09-27 10:00:00', 05, 01, 02, 02);
insert into registroCitas values (05, "Ernesto", "Bernarl", "Suarez", 12, 73581277172, "Cita Activa", 1300,
"El paciente es alergico al paracetamol", '2021-09-27 11:00:00', 03, 01, 01, 04);
select * from registroCitas;

create table cancelacion (
idCancelacion int auto_increment,
telefono varchar (50),
nota varchar (250),
fechaCancelacion datetime DEFAULT(NOW()),
idCitaCancelar int,
constraint pk_can primary key (idCancelacion),
constraint fk_ican foreign key (idCitaCancelar) references registroCitas (idCitas)
); 
insert into cancelacion values (01, "7778129300", "El cliente re agendara una cita nueva", '2021-09-23 15:33:00', 03 );
select * from cancelacion;

create table pago(
idPago int auto_increment, 
pagoTotal float,
notaPago varchar (250),
idCitaPago int,
constraint pk_ipa primary key (idPago),
constraint fk_icp foreign key (idCitaPago) references registroCitas (idCitas)
);
insert into pago values (01, 2500, "Se agrego al cargo una endodoncia", 01);
insert into pago values (02, 2300, "Se agrego limpieza bucal", 02);
insert into pago values (03, 3000, "Se agrego una endodoncia", 03);
insert into pago values (04, 1200, "Sin Cargos Extra",  04);
insert into pago values (05, 1300, "Sin Cargos Extra",  05);
select * from pago;

############################################################################################


Select * from registroCitas;
select * from empleados;
select * from pago;
#Una cita previamente registrada se puede cancelar, siempre y cuando no esté vencida 
update registroCitas set estado ="Cita Cancelada" where idCitas = 01;

#Registran y editan empleados. 
update empleados set correoElectronico="nuevocorreo@gmail.com", contraseña="nuevaContra", 
idConsultorioEmple=02, idClinicaEmpleado=02, estadoEmpleado="Inactivo" where idEmpleado=01;
#Eliminar empleados 
delete from empleados where idEmpleado=05;

#Consultan citas actuales y pasadas, para toda la clínica, por consultorio o médico. 
select idCitas as Folio, nombrePaciente as Nombre_Paciente, apellidoPatPaciente as Apellido_Paterno, apellidoMatPaciente as Apellido_Materno, 
estado, nombreEmpleado as Nombre_Doctor, apellidoPAtEmpleado, apellidoMatEmpleado, nombreClinica, claveC1 as Consultorio, date_format(fechaRegistro, "%d-%m-%Y %h:%i%p") as Fecha_Cita
from registroCitas 
inner join empleados on registroCitas.idEmpleRegis = idEmpleado
inner join clinicas on registroCitas.idClinicaRegis = idClinica
inner join consultorios on registroCitas.idConsultorioReg =  claveC1
;

#Médicos Consultan sus citas actuales y pasadas.
select  idCitas as Folio, nombreEmpleado as Nombre_Doctor, apellidoPAtEmpleado, apellidoMatEmpleado, claveC1 as Consultorio, date_format(fechaRegistro, "%d-%m-%Y %h:%i%p") as Fecha_Cita
from registroCitas
inner join empleados on registroCitas.idEmpleRegis = idEmpleado
inner join consultorios on registroCitas.idConsultorioReg =  claveC1;

#En las citas del día, deben confirmar si se atendió al paciente, confirmar el servicio realizado y confirmar el cobro correspondiente
update pago inner join registroCitas
on pago.idCitaPago = idCitas
set registroCitas.estado="Paciente Atendido", pago.pagoTotal=5000, notaPago="Se agrego una endodoncia"
where pago.idPago=05;

#Imprime el comprobante de pago que indica el día de la atención, el consultorio, 
#el médico que atendió, el servicio provisto y el monto total cobrado. 
select idCitas as Folio, date_format(fechaRegistro, "%d-%m-%Y %h:%i%p") as Fecha_Cita, claveC1 as Consultorio,
nombreEmpleado as Nombre_Doctor, apellidoPAtEmpleado, apellidoMatEmpleado, nombreServicio as Servicio_Inicial,
notaPago as Descripción, PagoTotal
from registroCitas 
inner join consultorios on registroCitas.idConsultorioReg =  claveC1
inner join empleados on registroCitas.idEmpleRegis = idEmpleado
inner join servicios on registroCitas.idServicioRegis = idServicio
inner join pago on registroCitas.idCitas = pago.idCitaPago;

#Puede consultar citas del día y pasadas de toda la clínica, de algún consultorio en particular o de algún médico en particular
select idCitas as Folio, date_format(fechaRegistro, "%d-%m-%Y %h:%i%p") as Fecha_Cita, claveC1 as Consultorio,
nombreEmpleado as Nombre_Doctor, apellidoPAtEmpleado, apellidoMatEmpleado, nombreServicio as Servicio_Inicial 
from registroCitas 
inner join consultorios on registroCitas.idConsultorioReg =  claveC1
inner join empleados on registroCitas.idEmpleRegis = idEmpleado
inner join servicios on registroCitas.idServicioRegis = idServicio
where nombreEmpleado="Teodulfo";