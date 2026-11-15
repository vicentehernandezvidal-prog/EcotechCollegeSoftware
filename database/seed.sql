-- =====================================================================
-- EcoTech Solutions - Datos de prueba
-- Compatible con database/schema.sql (MySQL / MariaDB)
--
-- Contenido:
--   2 administradores, 10 empleados, 4 departamentos, 5 proyectos,
--   18 asignaciones, 25 registros de tiempo y 4 informes.
--
-- IMPORTANTE - SEGURIDAD:
--   1) No se insertan datos personales sensibles en texto plano.
--      Las columnas direccion_cifrada, telefono_cifrado y salario_cifrado
--      quedan en NULL porque el proyecto entregado no define/implementa
--      un algoritmo ni una clave de cifrado verificable.
--   2) hash_password recibe SHA-256 de una contraseña de prueba mediante
--      la función de MySQL. Esto NO es bcrypt ni reemplaza un hash seguro
--      de producción. El código entregado tampoco implementa aún la
--      verificación de contraseñas (bcrypt aparece comentado en requirements).
--      Si la aplicación verifica con bcrypt, estos usuarios no podrán
--      autenticarse hasta generar los hashes con bcrypt desde Python.
--
-- Credencial de prueba asociada al hash SHA-256: EcoTech2026!
-- No reutilizar esta contraseña fuera de esta base de datos de pruebas.
--
-- Ejecutar después de crear la estructura con database/schema.sql.
-- Los IDs se especifican explícitamente para que las FK sean predecibles.
-- El script no elimina datos existentes. Ejecutarlo una sola vez sobre
-- una base vacía; si se vuelve a ejecutar, chocará con las claves únicas.
-- =====================================================================

USE ecotech;
START TRANSACTION;

-- ---------------------------------------------------------------------
-- 1. USUARIO: 2 administradores + 10 empleados
-- ---------------------------------------------------------------------
INSERT INTO USUARIO
    (id_usuario, nombre_usuario, hash_password, correo, rol)
VALUES
    (1,  'admin.sistema', UNHEX(SHA2('EcoTech2026!', 256)), 'admin.sistema@ecotech.test', 'ADMINISTRADOR'),
    (2,  'admin.proyectos', UNHEX(SHA2('EcoTech2026!', 256)), 'admin.proyectos@ecotech.test', 'ADMINISTRADOR'),
    (3,  'carlos.rojas', UNHEX(SHA2('EcoTech2026!', 256)), 'carlos.rojas@ecotech.test', 'EMPLEADO'),
    (4,  'andrea.munoz', UNHEX(SHA2('EcoTech2026!', 256)), 'andrea.munoz@ecotech.test', 'EMPLEADO'),
    (5,  'diego.torres', UNHEX(SHA2('EcoTech2026!', 256)), 'diego.torres@ecotech.test', 'EMPLEADO'),
    (6,  'camila.soto', UNHEX(SHA2('EcoTech2026!', 256)), 'camila.soto@ecotech.test', 'EMPLEADO'),
    (7,  'felipe.contreras', UNHEX(SHA2('EcoTech2026!', 256)), 'felipe.contreras@ecotech.test', 'EMPLEADO'),
    (8,  'valentina.diaz', UNHEX(SHA2('EcoTech2026!', 256)), 'valentina.diaz@ecotech.test', 'EMPLEADO'),
    (9,  'matias.fuentes', UNHEX(SHA2('EcoTech2026!', 256)), 'matias.fuentes@ecotech.test', 'EMPLEADO'),
    (10, 'sofia.morales', UNHEX(SHA2('EcoTech2026!', 256)), 'sofia.morales@ecotech.test', 'EMPLEADO'),
    (11, 'tomas.castillo', UNHEX(SHA2('EcoTech2026!', 256)), 'tomas.castillo@ecotech.test', 'EMPLEADO'),
    (12, 'isidora.vega', UNHEX(SHA2('EcoTech2026!', 256)), 'isidora.vega@ecotech.test', 'EMPLEADO');

-- ---------------------------------------------------------------------
-- 2. DEPARTAMENTO: gerente queda NULL temporalmente por la FK circular
-- ---------------------------------------------------------------------
INSERT INTO DEPARTAMENTO (id_departamento, nombre_dept, id_gerente)
VALUES
    (1, 'Desarrollo e Innovacion', NULL),
    (2, 'Ingenieria Ambiental', NULL),
    (3, 'Operaciones', NULL),
    (4, 'Administracion y Finanzas', NULL);

-- ---------------------------------------------------------------------
-- 3. EMPLEADO: 10 empleados. Datos sensibles cifrados quedan NULL.
--    RUT ficticios de prueba; no corresponden a personas reales.
-- ---------------------------------------------------------------------
INSERT INTO EMPLEADO
    (id_empleado, rut, id_usuario, id_departamento, primer_nombre,
     primer_apellido, direccion_cifrada, telefono_cifrado,
     inicio_contrato, salario_cifrado)
VALUES
    (1,  '11.111.111-1',  3, 1, 'Carlos',    'Rojas',       NULL, NULL, '2024-03-04', NULL),
    (2,  '11.111.111-2',  4, 1, 'Andrea',    'Munoz',       NULL, NULL, '2024-05-13', NULL),
    (3,  '11.111.111-3',  5, 2, 'Diego',     'Torres',      NULL, NULL, '2023-11-06', NULL),
    (4,  '11.111.111-4',  6, 2, 'Camila',    'Soto',        NULL, NULL, '2024-01-15', NULL),
    (5,  '11.111.111-5',  7, 3, 'Felipe',    'Contreras',   NULL, NULL, '2025-02-03', NULL),
    (6,  '11.111.111-6',  8, 3, 'Valentina', 'Diaz',        NULL, NULL, '2024-08-19', NULL),
    (7,  '11.111.111-7',  9, 1, 'Matias',    'Fuentes',     NULL, NULL, '2025-01-06', NULL),
    (8,  '11.111.111-8', 10, 4, 'Sofia',     'Morales',     NULL, NULL, '2023-09-11', NULL),
    (9,  '11.111.111-9', 11, 4, 'Tomas',     'Castillo',    NULL, NULL, '2025-04-21', NULL),
    (10, '11.111.112-0', 12, 2, 'Isidora',   'Vega',        NULL, NULL, '2025-06-02', NULL);

-- Asignar gerentes una vez que existen los empleados.
UPDATE DEPARTAMENTO SET id_gerente = 1 WHERE id_departamento = 1;
UPDATE DEPARTAMENTO SET id_gerente = 3 WHERE id_departamento = 2;
UPDATE DEPARTAMENTO SET id_gerente = 5 WHERE id_departamento = 3;
UPDATE DEPARTAMENTO SET id_gerente = 8 WHERE id_departamento = 4;

-- ---------------------------------------------------------------------
-- 4. ADMINISTRADOR
-- ---------------------------------------------------------------------
INSERT INTO ADMINISTRADOR (id_admin, id_usuario)
VALUES
    (1, 1),
    (2, 2);

-- ---------------------------------------------------------------------
-- 5. PROYECTO
-- ---------------------------------------------------------------------
INSERT INTO PROYECTO (id_proyecto, nombre, descripcion, fecha_inicio)
VALUES
    (1, 'Solar Norte',
     'Instalacion y monitoreo de paneles solares para infraestructura industrial.', '2025-01-15'),
    (2, 'Eolica Costa',
     'Evaluacion e implementacion de soluciones de generacion eolica costera.', '2025-04-01'),
    (3, 'Gestion Inteligente del Agua',
     'Desarrollo de sensores y plataforma para monitorear consumo y calidad del agua.', '2025-07-10'),
    (4, 'Edificios Sustentables',
     'Auditoria energetica y optimizacion de consumo en edificios.', '2025-09-01'),
    (5, 'Plataforma EcoData',
     'Desarrollo de plataforma de datos para consolidar indicadores ambientales.', '2026-01-12');

-- ---------------------------------------------------------------------
-- 6. ASIGNACION_PROYECTO: relaciones empleado-proyecto (muchos a muchos)
-- ---------------------------------------------------------------------
INSERT INTO ASIGNACION_PROYECTO (id_empleado, id_proyecto, fecha_asignacion)
VALUES
    (1, 1, '2025-01-15'), (1, 5, '2026-01-12'),
    (2, 1, '2025-01-20'), (2, 5, '2026-01-15'),
    (3, 2, '2025-04-01'), (3, 3, '2025-07-10'),
    (4, 2, '2025-04-03'), (4, 3, '2025-07-15'),
    (5, 1, '2025-02-01'), (5, 4, '2025-09-01'),
    (6, 2, '2025-04-10'), (6, 4, '2025-09-05'),
    (7, 5, '2026-01-12'), (7, 1, '2025-02-10'),
    (8, 4, '2025-09-01'),
    (9, 4, '2025-09-10'), (9, 5, '2026-01-20'),
    (10, 3, '2025-07-20');

-- ---------------------------------------------------------------------