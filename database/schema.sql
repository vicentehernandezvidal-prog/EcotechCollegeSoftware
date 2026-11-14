-- =====================================================================
-- schema.sql - Estructura de la base de datos de EcoTech Solutions
-- Motor: MySQL / MariaDB (XAMPP). Solo estructura, sin datos.
--
-- Uso: ejecutar UNA VEZ sobre un servidor sin la base "ecotech".
--   Opcion A (phpMyAdmin): pestaña "Importar" y elegir este archivo.
--   Opcion B (terminal):   mysql -u root -p < database/schema.sql
--
-- Para empezar de cero, descomenta la siguiente linea (BORRA todos los datos):
-- DROP DATABASE IF EXISTS ecotech;

-- =====================================================================

CREATE DATABASE IF NOT EXISTS ecotech CHARACTER SET utf8mb4;
USE ecotech;

-- ---------------------------------------------------------------------
-- USUARIO: datos comunes de acceso (base de Administrador y Empleado)
-- hash_password guarda el hash de la contraseña, nunca el texto plano
-- ---------------------------------------------------------------------
CREATE TABLE USUARIO (
  id_usuario     INT AUTO_INCREMENT PRIMARY KEY,
  nombre_usuario VARCHAR(50)    NOT NULL UNIQUE,
  hash_password  VARBINARY(255) NOT NULL,
  correo         VARCHAR(254)   NOT NULL UNIQUE,
  rol            VARCHAR(20)    NOT NULL,
  CHECK (rol IN ('ADMINISTRADOR', 'EMPLEADO'))
);

-- ---------------------------------------------------------------------
-- DEPARTAMENTO: id_gerente se enlaza a EMPLEADO mas abajo con ALTER TABLE,
-- porque EMPLEADO todavia no existe y se referencian entre si
-- ---------------------------------------------------------------------
CREATE TABLE DEPARTAMENTO (
  id_departamento INT AUTO_INCREMENT PRIMARY KEY,
  nombre_dept     VARCHAR(50) NOT NULL UNIQUE,
  id_gerente      INT NULL
);

-- ---------------------------------------------------------------------
-- EMPLEADO: datos propios del empleado (1 a 1 con USUARIO)
-- Las columnas *_cifrada/*_cifrado guardan datos sensibles ya cifrados
-- ---------------------------------------------------------------------
CREATE TABLE EMPLEADO (
  id_empleado       INT AUTO_INCREMENT PRIMARY KEY,
  rut               VARCHAR(12)  NOT NULL UNIQUE,
  id_usuario        INT          NOT NULL UNIQUE,
  id_departamento   INT          NOT NULL,
  primer_nombre     VARCHAR(100) NOT NULL,
  primer_apellido   VARCHAR(100) NOT NULL,
  direccion_cifrada VARBINARY(512),
  telefono_cifrado  VARBINARY(64),
  inicio_contrato   DATE         NOT NULL,
  salario_cifrado   VARBINARY(64),
  FOREIGN KEY (id_usuario)      REFERENCES USUARIO (id_usuario),
  FOREIGN KEY (id_departamento) REFERENCES DEPARTAMENTO (id_departamento)
);

-- Cierra la referencia circular: el gerente de un departamento es un empleado
ALTER TABLE DEPARTAMENTO
  ADD FOREIGN KEY (id_gerente) REFERENCES EMPLEADO (id_empleado);

-- ---------------------------------------------------------------------
-- ADMINISTRADOR: datos propios del administrador (1 a 1 con USUARIO)
-- ---------------------------------------------------------------------
CREATE TABLE ADMINISTRADOR (
  id_admin   INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL UNIQUE,
  FOREIGN KEY (id_usuario) REFERENCES USUARIO (id_usuario)
);

-- ---------------------------------------------------------------------
-- PROYECTO
-- ---------------------------------------------------------------------
CREATE TABLE PROYECTO (
  id_proyecto  INT AUTO_INCREMENT PRIMARY KEY,
  nombre       VARCHAR(150) NOT NULL,
  descripcion  VARCHAR(1000),
  fecha_inicio DATE         NOT NULL
);

-- ---------------------------------------------------------------------
-- ASIGNACION_PROYECTO: relacion muchos a muchos entre EMPLEADO y PROYECTO
-- La clave primaria compuesta evita asignar dos veces el mismo par
-- ---------------------------------------------------------------------
CREATE TABLE ASIGNACION_PROYECTO (
  id_empleado      INT  NOT NULL,
  id_proyecto      INT  NOT NULL,
  fecha_asignacion DATE NOT NULL,
  PRIMARY KEY (id_empleado, id_proyecto),
  FOREIGN KEY (id_empleado) REFERENCES EMPLEADO (id_empleado),
  FOREIGN KEY (id_proyecto) REFERENCES PROYECTO (id_proyecto)
);

-- ---------------------------------------------------------------------
-- REGISTRO_TIEMPO: horas trabajadas por un empleado en un proyecto
-- ---------------------------------------------------------------------
CREATE TABLE REGISTRO_TIEMPO (
  id_registro       INT AUTO_INCREMENT PRIMARY KEY,
  id_empleado       INT           NOT NULL,
  id_proyecto       INT           NOT NULL,
  fecha             DATE          NOT NULL,
  horas             DECIMAL(4,2)  NOT NULL,
  descripcion_tarea VARCHAR(500),
  estado_validacion VARCHAR(15)   NOT NULL DEFAULT 'PENDIENTE',
  FOREIGN KEY (id_empleado) REFERENCES EMPLEADO (id_empleado),
  FOREIGN KEY (id_proyecto) REFERENCES PROYECTO (id_proyecto),
  CHECK (horas > 0 AND horas <= 24),
  CHECK (estado_validacion IN ('PENDIENTE', 'APROBADO', 'RECHAZADO'))
);

-- ---------------------------------------------------------------------
-- INFORME: informes generados por un administrador
-- ---------------------------------------------------------------------
CREATE TABLE INFORME (
  id_informe       INT AUTO_INCREMENT PRIMARY KEY,
  id_admin         INT         NOT NULL,
  tipo_contenido   VARCHAR(50) NOT NULL,
  formato          VARCHAR(10) NOT NULL,
  fecha_generacion DATETIME    NOT NULL,
  FOREIGN KEY (id_admin) REFERENCES ADMINISTRADOR (id_admin),
  CHECK (formato IN ('PDF', 'EXCEL'))
);