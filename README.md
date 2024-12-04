# Proyecto de Arquitectura de Software

Este es un proyecto de ejemplo desarrollado en Flask que implementa un sistema cliente-servidor con PostgreSQL como base de datos. El proyecto incluye funcionalidades de autenticación, gestión de usuarios y algunas operaciones CRUD relacionadas.  
**RAMA MÁS ACTUALIZADA**: `rama2`

## Tabla de Contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

---

## Características

- Implementación del patrón **MVC**.
- Autenticación de usuarios con **Flask-Login**.
- Encriptación de contraseñas con **bcrypt**.
- Gestión de base de datos con **Flask-SQLAlchemy** y **Flask-Migrate**.
- Conexión a **PostgreSQL**.
- Modularización de rutas mediante **Blueprints**.

---

## Tecnologías

Este proyecto utiliza las siguientes herramientas y tecnologías:

- **Python 3.x**
- **Flask**
  - Flask-SQLAlchemy
  - Flask-Migrate
  - Flask-Login
- **PostgreSQL**
- **bcrypt** para el manejo de contraseñas
- **Jinja2** para plantillas HTML

---

## Requisitos Previos

Asegúrate de tener instalados los siguientes elementos antes de comenzar:

1. **Python 3.x**  
2. **PostgreSQL**  
3. **Git**  
4. **Virtualenv** (opcional, pero recomendado).

---

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu_usuario/nombre_del_repositorio.git
   cd nombre_del_repositorio

   
Crear y activar un entorno virtual:

bash
Copy code
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Instalar las dependencias:

bash
Copy code
pip install -r requirements.txt
Configurar la base de datos:

Crear una base de datos en PostgreSQL.
Actualizar la URI de la base de datos en app.config dentro del archivo create_app:
python
Copy code
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:contraseña@host:puerto/nombre_base_datos'
Migrar la base de datos:

bash
Copy code
flask db init
flask db migrate -m "Inicializar base de datos"
flask db upgrade
Ejecutar la aplicación:

bash
Copy code
flask run
La aplicación estará disponible en http://localhost:5000.
