# EcoTech Solutions — versión migrada (ES3)

Proyecto académico de consola desarrollado en Python y MySQL. Esta versión traslada las entidades, repositorios y menús del proyecto anterior a una estructura modular y agrega autenticación, validación, manejo de errores y consumo de dos servicios externos.

## Estructura 

- `entidades/`: clases del dominio y herencia de Usuario.
- `repositorios/`: operaciones SQL parametrizadas.
- `database/`: conexión y esquema MySQL.
- `seguridad/`: hash de contraseñas mediante PBKDF2-HMAC-SHA256.
- `servicios/`: autenticación, clima y divisas.
- `menus/`: interacción por consola.

## Requisitos

Tecnologias: 
- Python 3.10 o superior.
- MySQL/MariaDB (por ejemplo, XAMPP).

Librerias: 
- PyMySQL
- Python dotenv 
- request 
- bcrypt
- cryptography


## Instalación

1. Crear un entorno virtual: `python -m venv .venv`
2. Activarlo.
3. Instalar dependencias: `pip install -r requirements.txt`
4. Copiar `.env.example` a `.env` y configurar las credenciales locales de MySQL.
5. Importar `database/schema.sql` desde phpMyAdmin o MySQL.
6. Ejecutar `python main.py`.

La primera ejecución permite crear el primer administrador. Los usuarios empleados también pueden iniciar sesión; el registro, modificación y eliminación de cuentas y la gestión de informes quedan reservados al rol administrador. Las contraseñas se almacenan como hash con sal individual; no se guardan en texto plano.

## APIs

- Clima: Open-Meteo (geocodificación y condiciones actuales).
- Divisas: DolarAPI Chile (`https://cl.dolarapi.com/v1/cotizaciones`).

Ambas consultas usan `requests`, timeout, validación básica y control de errores HTTP/conexión.

## Referencias técnicas de las APIs

- Open-Meteo: https://open-meteo.com/en/docs
- DolarAPI Chile: https://dolarapi.com/docs/chile/operations/get-cotizaciones

## Consideraciones

- `.env` está excluido de Git. 
- Software estrictamente academico 
