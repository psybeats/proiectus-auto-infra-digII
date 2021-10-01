create database clinicaDental;
use clinicaDental;

create table clinicas(
idClinica int auto_increment,
nombreClinica varchar (255),
direcccion varchar (255),
telefono varchar (50),
constraint pk_ic primary key (idClinica)
);

create table servicios(
idServicio int,
nombreServicio varchar (255),
costoServicio float,
constraint pk_is primary key (idServicio)
);
#insert into servicios values (01, "extraccion de muela", 500);

create table pacientes(
idPaciente int PRIMARY KEY auto_increment,
nombrePaciente varchar(30),
apellidoPaciente varchar(20),
edad int,
telefono varchar(50),
direccion varchar(255),
tipoServicio int,
fechaEntrada datetime DEFAULT(NOW()),
constraint fk_ts foreign key(tipoServicio) references servicios(idServicio)
);
#insert into pacientes values (001, 'Jose', 'Perez', 23, 'San cristobal', 01, '2021-09-27 10:00:00');

create table odontologos(
idOdontologo int auto_increment,
nombreOdontologo varchar(255),
apellidoOdontologo varchar(255),
rolOdontologo varchar (50),
cedulaProfesional varchar(255),
direccion varchar(255),
idClinica1 int,
constraint pk_io primary key (idOdontologo),
constraint fk_id foreign key (idClinica1) references clinicas (idClinica)
);
#insert into odontologos values (001, 'Alfredo', 'Rios', '12818ns1', 'san juan');

create table consultorio1(
claveC1 int auto_increment,
horario varchar (12),
idPaciente1 int,
idOdontologo1 int,
idServicio1 int,
constraint pk_io primary key (claveC1),
constraint fk_fip foreign key (idPaciente1) references pacientes (idPaciente),
constraint fk_fio foreign key (idOdontologo1) references odontologos (idOdontologo),
constraint fk_fts foreign key (idServicio1) references servicios (idServicio)
);

create table consultorio2(
claveC2 int auto_increment,
horario2 varchar (12),
idPaciente2 int,
idOdontologo2 int,
idServicio2 int,
constraint pk_io primary key (claveC2),
constraint fk_fip2 foreign key (idPaciente2) references pacientes (idPaciente),
constraint fk_fio2 foreign key (idOdontologo2) references odontologos (idOdontologo),
constraint fk_fts3 foreign key (idServicio2) references servicios (idServicio)
);
#insert into consultorio2 values (001, 'vespertino', 1, 01, 11);

create table registroCitas (
idCitas int primary key auto_increment,
estado varchar(50),
nombrePaciente varchar(255),
idPaciente5 int,
fechaEntrada datetime DEFAULT(NOW()),
idServicio3 int,
constraint fk_is3 foreign key  (idServicio3) references servicios (idServicio),
constraint fk_ip foreign key (idPaciente5) references pacientes (idPaciente)
);