from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt


# Inicializa la base de datos
db = SQLAlchemy()

# Inicializa Flask-Migrate
migrate = Migrate()

login_manager = LoginManager()


def create_app():
    app = Flask(__name__,static_folder='../static', template_folder='../templates')  # Asegúrate de poner la ruta correcta
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:contraseña@ip:5432/aes_project'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.secret_key = 'your-secret-key'  # Necesario para las sesiones

    # Configurar LoginManager
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # Redirige a la vista 'login' si el usuario no está autenticado
    
    
    
    # Inicializa las extensiones
    db.init_app(app)
    migrate.init_app(app, db)
 
    # Importar y registrar las rutas
    from .views import views_blueprint
    app.register_blueprint(views_blueprint)
 
    return app
