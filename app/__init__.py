from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Inicializa la base de datos
db = SQLAlchemy()

# Inicializa Flask-Migrate
migrate = Migrate()

def create_app():
    app = Flask(__name__,static_folder='../static', template_folder='../templates')  # Asegúrate de poner la ruta correcta
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:contraseña@ip-sistema_operativo_con_postgre:5432/nombre_base_de_datos'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa las extensiones
    db.init_app(app)
    migrate.init_app(app, db)
 
    # Importar y registrar las rutas
    from .views import views_blueprint
    app.register_blueprint(views_blueprint)
 
    return app
