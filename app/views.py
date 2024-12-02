from flask import Flask, Blueprint, request, jsonify, render_template
from .models import User, Category, Promotion, Pizza, ShoppingCart
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

        # Validar que los campos no estén vacíos
        if not email_or_username or not password:
            flash('Por favor ingresa tu email o nombre de usuario y la contraseña', 'error')
            return redirect(url_for('views_blueprint.login'))

        # Buscar al usuario por email o username
        user = User.query.filter((User.email == email_or_username) | (User.username == email_or_username)).first()

        if user and user.check_password(password):  # Verifica la contraseña
            login_user(user)  # Inicia sesión
            return redirect(url_for('views.index'))  # Redirige a la página principal
        else:
            flash('Email, nombre de usuario o contraseña incorrectos', 'error')  # Error si no coincide

    return render_template('auth/login.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




from werkzeug.security import generate_password_hash
from flask import flash, redirect, render_template, request
from app import db
from app.models import User

import requests  # Importa requests para manejar el webhook

@views_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener los valores del formulario
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        document_type = request.form.get('document_type')
        document_number = request.form.get('document_number')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validaciones
        if password != confirm_password:
            flash("Las contraseñas no coinciden", "error")
            return redirect('/register')

        if not (first_name and last_name and document_type and document_number and phone_number and email and password):
            flash("Por favor, complete todos los campos obligatorios", "error")
            return redirect('/register')

        username = f"{first_name.lower()}{last_name.lower()}"
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("El nombre de usuario ya está en uso, por favor elige otro.", "error")
            return redirect('/register')

        # Hash de la contraseña y crear usuario
        hashed_password = generate_password_hash(password)
        user = User(
            first_name=first_name,
            last_name=last_name,
            document_type=document_type,
            document_number=document_number,
            phone_number=phone_number,
            email=email,
            username=username,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        # Webhook: notificar registro exitoso
        webhook_url = "https://webhook-test.com/18c89d7118757a929fd629ed576a9e56"  # Cambiar a la URL del webhook real
        payload = {
            "event": "user_registered",
            "data": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "document_type": document_type,
                "document_number": document_number,
                "phone_number": phone_number,
            }
        }
        try:
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 200:
                print("Webhook enviado exitosamente.")
            else:
                print(f"Error al enviar webhook: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error al enviar el webhook: {e}")

        # Redirigir al usuario al login
        flash("¡Te has registrado exitosamente! Ahora puedes iniciar sesión.", "success")
        return redirect('/login')

    # Si el método es GET, se muestra el formulario de registro
    return render_template('auth/register.html')

from flask_login import login_required, current_user

@views_blueprint.route('/profile')
@login_required  # Esta decorador asegura que el usuario esté autenticado
def profile():
    return render_template('profile.html', user=current_user)

@views_blueprint.route('/logout')
@login_required  # Asegura que el usuario esté autenticado antes de poder cerrar sesión
def logout():
    logout_user()  # Cierra la sesión del usuario
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('views.login'))

@views_blueprint.route('/dashboard')
@login_required  # Sólo los usuarios autenticados pueden acceder
def dashboard():
    if current_user.is_authenticated:
        # Aquí, `current_user` tiene todos los datos del usuario
        return render_template('dashboard.html', user=current_user)
    else:
        flash('Debes iniciar sesión para acceder al dashboard', 'error')
        return redirect(url_for('views.login'))

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

# Carrito
@views_blueprint.route('/add_to_cart/pizza/<int:pizza_id>', methods=['POST'])
def add_pizza_to_cart(pizza_id):
    if not current_user.is_authenticated:
        flash("Por favor, inicia sesión para agregar productos al carrito.", "error")
        return redirect('/login')

    quantity = request.form.get('quantity', 1)

    # Verificar si la pizza ya existe en el carrito
    existing_item = ShoppingCart.query.filter_by(user_id=current_user.id, pizza_id=pizza_id).first()
    if existing_item:
        existing_item.quantity += int(quantity)
    else:
        new_item = ShoppingCart(user_id=current_user.id, pizza_id=pizza_id, quantity=int(quantity))
        db.session.add(new_item)

    db.session.commit()
    flash("Producto agregado al carrito.", "success")
    return redirect('/')


@views_blueprint.route('/add_to_cart/promotion/<int:promotion_id>', methods=['POST'])
def add_promotion_to_cart(promotion_id):
    if not current_user.is_authenticated:
        flash("Por favor, inicia sesión para agregar productos al carrito.", "error")
        return redirect('/login')

    # Aquí debes agregar la lógica para agregar una promoción al carrito
    # Por ejemplo, podrías almacenar la promoción en una tabla similar a la de las pizzas en el carrito

    flash("Promoción agregada al carrito.", "success")
    return redirect(url_for('views.promociones'))  # Redirigir a la vista de promociones


@views_blueprint.route('/cart')
def view_cart():
    if not current_user.is_authenticated:
        flash("Por favor, inicia sesión para ver tu carrito.", "error")
        return redirect('/login')

    cart_items = ShoppingCart.query.filter_by(user_id=current_user.id).all()

    cart_details = []
    for item in cart_items:
        pizza = Pizza.query.get(item.pizza_id)
        cart_details.append({
            'id': item.id,
            'name': pizza.name,
            'price': pizza.price,
            'quantity': item.quantity,
            'subtotal': pizza.price * item.quantity
        })

    total = sum([item['subtotal'] for item in cart_details])

    return render_template('cart.html', cart_details=cart_details, total=total)

@views_blueprint.route('/remove_from_cart/<int:cart_item_id>', methods=['POST'])
def remove_from_cart(cart_item_id):
    if not current_user.is_authenticated:
        flash("Por favor, inicia sesión para modificar tu carrito.", "error")
        return redirect('/login')

    cart_item = ShoppingCart.query.get(cart_item_id)
    if not cart_item or cart_item.user_id != current_user.id:
        flash("Producto no encontrado en tu carrito.", "error")
        return redirect('/cart')

    db.session.delete(cart_item)
    db.session.commit()
    flash("Producto eliminado del carrito.", "success")
    return redirect('/cart')




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


