🎮 PS3 Digital Store API (FastAPI + PostgreSQL Transaccional)

API de backend desarrollada con FastAPI, enfocada en la lógica de negocio y transaccional para una tienda digital de videojuegos (modelo similar al de PlayStation Store).

Este proyecto utiliza PostgreSQL (a través de Supabase) con transacciones ACID para garantizar la integridad de los datos, asegurando que el saldo se descuente y la compra se registre simultáneamente, o que falle completamente.

✨ Características Principales

Transacciones ACID: Uso de psycopg.connect.commit() y conn.rollback() para garantizar que las operaciones de compra (descuento de saldo + registro de compra) sean atómicas y consistentes.

Bloqueo de Filas (FOR UPDATE): Implementación de bloqueos a nivel de fila para prevenir condiciones de carrera al verificar y descontar el saldo del cliente en compras concurrentes.

Patrón de Repositorio: Lógica de base de datos separada en clases (ClienteRepository, JuegoRepository, CompraRepository) para mantener el código de la API limpio.

Validación de Modelos: Uso de Pydantic para validar los datos de entrada (ej. asegurar que los precios sean mayores a 0).

Documentación Interactiva: Exposición automática de la API en /docs (Swagger UI).

Seguridad: Uso de variables de entorno (.env) y .gitignore para proteger las credenciales de la base de datos.

⚙️ Configuración y Ejecución Local

Sigue estos pasos para levantar la API en tu entorno local.

1. Requisitos Previos

Python 3.10+

Gestor de paquetes pip

Una base de datos PostgreSQL activa (se recomienda Supabase).

2. Configuración de la Base de Datos (Supabase)

Asegúrate de haber creado las tres tablas requeridas (cliente, juego, compra) con sus respectivas claves primarias (PK) y foráneas (FK) en Supabase.

Las credenciales de conexión se obtienen de la sección de Configuración de la Base de Datos de Supabase.

3. Entorno Virtual e Instalación de Dependencias

Se recomienda encarecidamente usar un entorno virtual (venv):

# 1. Crear el entorno virtual
python -m venv venv

# 2. Activar el entorno (Windows)
# Si usas PowerShell:
# .\venv\Scripts\activate
# Si usas CMD:
# .\venv\Scripts\activate.bat

# 3. Instalar las dependencias necesarias
# psycopg es el driver de PostgreSQL
# python-dotenv para leer bd.env
pip install fastapi uvicorn psycopg-binary python-dotenv




4. Configuración de Credenciales (.env)

Crea un archivo llamado bd.env en la raíz del proyecto. Este archivo contiene la contraseña de tu base de datos y está ignorado por Git por seguridad.

# Contraseña de la base de datos de PostgreSQL/Supabase
PASSWORD=TU_CONTRASEÑA_SECRETA_DE_SUPABASE




5. Ejecución del Servidor

Inicia el servidor Uvicorn en modo de recarga automática (reload):

uvicorn main:app --reload




El servidor estará disponible en: http://127.0.0.1:8000

🧪 Uso y Endpoints Clave

Una vez que el servidor esté activo, puedes interactuar con la API a través de la documentación interactiva: http://127.0.0.1:8000/docs

Ruta

Método

Descripción

/cliente/registrar

POST

Registra un nuevo cliente con saldo inicial.

/cliente/{cliente_id}

GET

Muestra el saldo y los datos de un cliente.

/compra/finalizar

POST

Ejecuta la transacción crítica. Descuenta el saldo y registra la compra.

/biblioteca/{cliente_id}

GET

Muestra todos los juegos comprados por un cliente.

/catalogo/agregar_juego

POST

Agrega un nuevo juego al catálogo.

🙏 Agradecimientos

La estructura inicial, las clases de repositorio, la lógica de transacciones con FOR UPDATE, la arquitectura de la API y esta misma documentación (README.md) fueron desarrollados con la asistencia y guía de Gemini.

Hecho con por Germán Fredes
