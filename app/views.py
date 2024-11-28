from flask import Flask, Blueprint, request, jsonify, render_template
from .models import User, Category, Promotion, Pizza
from . import db, login_manager
from flask import flash, redirect, url_for
from flask_login import login_user, logout_user


views_blueprint = Blueprint('views', __name__, template_folder='../templates')

# Inicializar el diccionario para almacenar las promociones por categoría

@views_blueprint.route('/')
@views_blueprint.route('/index')
def index():
    categories = Category.query.all()
    promotions_data = {}

    for category in categories:
        promotions = Promotion.query.filter(Promotion.category_id == category.id).all()
        promotions_data[category.name] = promotions

    print(promotions_data)  # Verifica si los datos están bien organizados

    return render_template('index.html', promotions_data=promotions_data)

@views_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtén los datos del formulario
        email_or_username = request.form.get('email_or_username')  # Campo único para email o username
        password = request.form.get('password')

        if not email_or_username or not password:
            flash('Por favor ingresa tu email o nombre de usuario y la contraseña', 'error')
            return redirect(url_for('views_blueprint.login'))

        # Buscar al usuario por email o username
        user = User.query.filter((User.email == email_or_username) | (User.username == email_or_username)).first()

        if user and user.check_password(password):  # Verifica la contraseña
            login_user(user)  # Inicia sesión
            return redirect(url_for('index'))  # Redirige a la página principal
        else:
            flash('Email, nombre de usuario o contraseña incorrectos', 'error')  # Error si no coincide

    return render_template('auth/login.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@views_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener los valores del formulario
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')

        # Validar que las contraseñas coincidan
        if password != confirm_password:
            flash("Las contraseñas no coinciden", "error")
            return redirect('/auth/register')

        # Validar que todos los campos obligatorios estén completos
        if not (username and password and email):
            flash("Por favor, complete todos los campos obligatorios", "error")
            return redirect('/auth/register')

        # Crear el nuevo usuario
        user = User(username=username, password=password, email=email)

        # Guardar el usuario en la base de datos
        db.session.add(user)
        db.session.commit()

        flash("¡Te has registrado exitosamente! Ahora puedes iniciar sesión.", "success")
        return redirect('/auth/login')

    return render_template('auth/register.html')

@views_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Crear el blueprint
promotions_bp = Blueprint('promotions', __name__)

# Definir la ruta para mostrar las promociones
@promotions_bp.route('/promotions')
def promotions():
    filter_type = request.args.get('filter')  # Obtener el parámetro de filtro
    
    # Si hay un filtro, busca las promociones correspondientes
    if filter_type:
        promotions = Promotion.query.filter(Promotion.category_type == filter_type).all()
    else:
        # Si no hay filtro, mostrar todas las promociones
        promotions = Promotion.query.all()
    
    return render_template('promotions.html', promotions=promotions)

@views_blueprint.route('/promociones/promociones')
def promociones():
    categories = Category.query.all()
    promotions_data = {}

    for category in categories:
        promotions = Promotion.query.filter(Promotion.category_id == category.id).all()
        promotions_data[category.name] = promotions

    print(promotions_data)  # Verifica si los datos están bien organizados

    return render_template('promociones/promociones.html', promotions_data=promotions_data)

from flask import render_template, request
from .models import Promotion, Pizza

@views_blueprint.route('/search')
def search():
    query = request.args.get('query', '').strip().lower()  # Obtener la consulta de búsqueda
    resultados = []

    if query:
        # Buscar en las promociones
        promociones_resultados = Promotion.query.filter(
            (Promotion.title.ilike(f"%{query}%")) | 
            (Promotion.description.ilike(f"%{query}%"))
        ).all()

        # Buscar en las pizzas (suponiendo que hay un modelo llamado Pizza)
        pizzas_resultados = Pizza.query.filter(
            (Pizza.name.ilike(f"%{query}%")) | 
            (Pizza.description.ilike(f"%{query}%"))
        ).all()

        # Combinar los resultados de promociones y pizzas
        resultados = []
        
        for promo in promociones_resultados:
            resultados.append({
                'type': 'promotion',
                'title': promo.title,
                'description': promo.description,
                'image': promo.image,
                'price': promo.price
            })
        
        for pizza in pizzas_resultados:
            resultados.append({
                'type': 'pizza',
                'title': pizza.name,
                'description': pizza.description,
                'image': pizza.image,
                'price': pizza.price
            })

    return render_template('search.html', query=query, resultados=resultados)


@views_blueprint.route('/pizzas/pizzas', methods=['GET'])
def mostrar_pizzas():
    category = request.args.get('category')  # Obtiene la categoría de la URL
    if category:
        pizzas = Pizza.query.filter_by(category_id=category).all()
    else:
        pizzas = Pizza.query.all()  # Muestra todas si no hay filtro
    return render_template('pizzas/pizzas.html', pizzas=pizzas)



@views_blueprint.route('/combos/combos')
def combos():
    combos = Promotion.query.filter(Promotion.title.ilike('%Combo%')).all()  # Filtramos las promociones que tienen 'Combo' en el título
    return render_template('combos/combos.html', combos=combos)


@views_blueprint.route('/miPlantilla')
def layout():
    """Página principal para visualizar promociones y la ubicación del repartidor"""
    return render_template('layout.html')

@views_blueprint.route('/navbar')
def navbar():
    """Página principal para visualizar promociones y la ubicación del repartidor"""
    return render_template('navbar.html')

@views_blueprint.route('/pizzas/clasicas')
def clasicas():
    return render_template('pizzas/clasicas.html', filter="5amas")

@views_blueprint.route('/pizzas/especialidades')
def especialidades():
    return render_template('pizzas/especialidades.html', filter="5amas")

@views_blueprint.route('/contactanos')
def contactanos():
    """Página para contacto"""
    return render_template('contactanos.html')

@views_blueprint.route('/rastreo')
def rastreo():
    """Página para el repartidor que envía la ubicación en tiempo real"""
    return render_template('rastreo.html')



# Rutas para la ubicación del repartidor
ubicacion_repartidor = {"lat": None, "lon": None}

@views_blueprint.route('/actualizar_ubicacion', methods=['POST'])
def actualizar_ubicacion():
    """Recibe la ubicación actual del repartidor desde el móvil"""
    data = request.get_json()
    lat = data.get("lat")
    lon = data.get("lon")

    # Actualiza la ubicación en la memoria
    ubicacion_repartidor["lat"] = lat
    ubicacion_repartidor["lon"] = lon

    return jsonify({"mensaje": "Ubicación actualizada correctamente"}), 200

@views_blueprint.route('/obtener_ubicacion', methods=['GET'])
def obtener_ubicacion():
    """Devuelve la ubicación actual del repartidor"""
    if ubicacion_repartidor["lat"] is not None and ubicacion_repartidor["lon"] is not None:
        return jsonify({"ubicacion": ubicacion_repartidor})
    else:
        return jsonify({"mensaje": "Ubicación no disponible"}), 404


