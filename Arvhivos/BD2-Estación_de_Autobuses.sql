create database estacionAutobus;
use estacionAutobus;

create table choferes(
idChofer int primary key auto_increment,
nombreChofer varchar (255),
apellidoCofer varchar (255)
);

create table usuarios(
idUser int primary key auto_increment,
nombreUser varchar (255),
apellidosUser varchar (255),
telefonoUser varchar (255),
direccion varchar (50),
contraseña varchar (50) NOT NULL
);

create table autobuses(
idAutobus int primary key auto_increment,
numAutobus int,
capacidad int,
idchoferAuto int,
constraint fk_ica foreign key (idchoferAuto) references choferes (idChofer)
);

create table destinos(
idDestino int primary key auto_increment,
ciudadDestino varchar (255),
idAutobusDes int,
constraint fk_iad foreign key (idAutobusDes) references autobuses (idAutobus)
);

create table horarios(
idHorario int primary key auto_increment,
horaSal time,
horallegada time,
idAutobusH int,
idDestinoH int,
constraint fk_iah foreign key (idAutobusH) references autobuses (idAutobus),
constraint fk_idh foreign key (idDestinoH) references destinos (idDestino)
);

create table horario_destino(
clave_idHorario int,
clave_idDestino int,
constraint fk_cih foreign key (clave_idHorario) references horarios (idHorario),
constraint fk_cid foreign key (clave_idDestino) references destinos (idDestino)
);

create table reservaciones (
idReservacion int primary key auto_increment,
fechaReservacion date,
validacion varchar (50),
idHorarioR int,
idUsuarioR int,
idDestinoR int,
constraint fk_ihr foreign key (idHorarioR) references horarios (idHorario),
constraint fk_iur foreign key (idUsuarioR) references usuarios(idUser),
constraint fk_idr foreign key (idDestinoR) references destinos (idDestino)
);