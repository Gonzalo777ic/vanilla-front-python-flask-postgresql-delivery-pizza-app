from flask import Flask, Blueprint, request, jsonify, render_template
from .models import User, Category, Promotion, Pizza, ShoppingCart, Order, ShoppingCart, OrderPizza, OrderPromotion, PaymentMethod, ShippingAddress, PurchaseHistory, Notification
from . import db, login_manager
from flask import flash, redirect, url_for
from flask_login import login_user, logout_user



views_blueprint = Blueprint('views', __name__, template_folder='../templates')

# Inicializar el diccionario para almacenar las promociones por categoría

@views_blueprint.route('/')
@views_blueprint.route('/index')
def index():
    category = request.args.get('category')  # Obtener la categoría desde los parámetros de la URL

    if category:
        # Filtrar por categoría tanto pizzas como promociones
        pizzas = Pizza.query.filter_by(category_id=category).all()
        promociones = Promotion.query.filter_by(category_id=category).all()
    else:
        # Mostrar todas las pizzas y promociones si no hay filtro
        pizzas = Pizza.query.all()
        promociones = Promotion.query.all()

    categories = Category.query.all()  # Si necesitas las categorías
    promotions_data = {}

    for category in categories:
        promotions = Promotion.query.filter(Promotion.category_id == category.id).all()
        promotions_data[category.name] = promotions

    # Renderizar el template pasando ambas listas
    return render_template(
        'index.html',
        pizzas=pizzas,
        promociones=promociones,
        promotions_data=promotions_data
    )

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
        webhook_url = "https://webhook-test.com/1c8b8262c234f641a7490c73b17b10cf"  # Cambiar a la URL del webhook real
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

@views_blueprint.route('/promociones/promociones', methods=['GET'])
def mostrar_promociones():
    category = request.args.get('category')  # Obtiene la categoría de la URL
    if category:
        # Filtra las promociones por categoría
        promociones = Promotion.query.filter_by(category_id=category).all()  # Filtrar categorías
    else:
        # Si no hay filtro, obtenemos todas las categorías
        promociones = Promotion.query.all()
    return render_template('promociones/promociones.html', promociones=promociones)

@views_blueprint.route('/combos', methods=['GET'])
def mostrar_combos():
    category = request.args.get('category')  # Obtén la categoría desde los parámetros de la URL
    if category:
        combos = Promotion.query.filter_by(category_id=category).filter(Promotion.title.ilike('%combo%')).all()
    else:
        combos = Promotion.query.filter(Promotion.title.ilike('%combo%')).all()  # Mostrar solo promociones con "combo"
    return render_template('combos/combos.html', combos=combos)



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
    quantity = request.form.get('quantity', 1)

    # Verificar si la pizza ya existe en el carrito
    existing_item = ShoppingCart.query.filter_by(user_id=current_user.id, promotion_id=promotion_id).first()
    if existing_item:
        existing_item.quantity += int(quantity)
    else:
        new_item = ShoppingCart(user_id=current_user.id, promotion_id=promotion_id, quantity=int(quantity))
        db.session.add(new_item)

    db.session.commit()
    # Aquí debes agregar la lógica para agregar una promoción al carrito
    # Por ejemplo, podrías almacenar la promoción en una tabla similar a la de las pizzas en el carrito

    flash("Promoción agregada al carrito.", "success")
    return redirect(url_for('views.mostrar_promociones'))  # Redirigir a la vista de promociones

@views_blueprint.route('/cart')
def view_cart():
    if not current_user.is_authenticated:
        flash("Por favor, inicia sesión para ver tu carrito.", "error")
        return redirect('/login')

    cart_items = ShoppingCart.query.filter_by(user_id=current_user.id).all()

    cart_details = []
    for item in cart_items:
        # Verificar si es una pizza o una promoción
        pizza = Pizza.query.get(item.pizza_id)  # Obtener pizza
        promotion = Promotion.query.get(item.promotion_id)  # Obtener promoción

        if pizza:
            # Si el item es una pizza
            cart_details.append({
                'id': item.id,
                'name': pizza.name,
                'price': pizza.price,
                'quantity': item.quantity,
                'subtotal': pizza.price * item.quantity
            })
        elif promotion:
            # Si el item es una promoción
            cart_details.append({
                'id': item.id,
                'name': promotion.title,  # Usamos el título de la promoción
                'price': promotion.price,
                'quantity': item.quantity,
                'subtotal': promotion.price * item.quantity
            })
        else:
            # Si el item no es una pizza ni una promoción (error o invalid)
            cart_details.append({
                'id': item.id,
                'name': 'Producto no disponible',
                'price': 0,
                'quantity': item.quantity,
                'subtotal': 0
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


@views_blueprint.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not current_user.is_authenticated:
        # Redirigir a la página de login si no está autenticado
        return redirect(url_for('auth.login'))

    # Obtener las direcciones de envío del usuario
    shipping_addresses = ShippingAddress.query.filter_by(user_id=current_user.id).all()

    return render_template('checkout.html', user=current_user, shipping_addresses=shipping_addresses)


from flask import redirect, url_for


from flask_login import current_user, login_required

@views_blueprint.route('/buy', methods=['POST'])
@login_required
def buy():
    user = current_user
    payment_method_name = request.form.get('payment_method') 
    payment_method = PaymentMethod.query.filter_by(id=payment_method_name).first()
    print(payment_method)

    # Obtener el carrito del usuario
    cart_items = ShoppingCart.query.filter_by(user_id=user.id).all()

    # Calcular el precio total del carrito, considerando tanto pizzas como promociones
    total_price = 0
    for item in cart_items:
        # Verificar si el item es una pizza o una promoción
        pizza = Pizza.query.get(item.pizza_id)  # Obtener pizza
        promotion = Promotion.query.get(item.promotion_id)  # Obtener promoción

        if pizza:
            # Si el item es una pizza
            total_price += pizza.price * item.quantity
        elif promotion:
            # Si el item es una promoción
            total_price += promotion.price * item.quantity
        else:
            # Si el item no es ni una pizza ni una promoción, esto podría ser un error
            flash("Producto no disponible", "error")
            return redirect(url_for('views.cart'))

    # Crear la nueva orden
    new_order = Order(
        user_id=user.id,
        total_price=total_price,
        status='Pendiente',  # Puedes ajustar el estado según el proceso de pago
        payment_method_id=payment_method.id
    )
    db.session.add(new_order)
    db.session.commit()  # Guardar la orden

    # Transferir los productos del carrito a la orden
    for item in cart_items:
        pizza = Pizza.query.get(item.pizza_id)
        promotion = Promotion.query.get(item.promotion_id)

        if pizza:
            order_pizza = OrderPizza(order_id=new_order.id, pizza_id=item.pizza.id, quantity=item.quantity, price=pizza.price)
            db.session.add(order_pizza)
        elif promotion:
            order_promotion = OrderPromotion(order_id=new_order.id, promotion_id=item.promotion_id, quantity=item.quantity, price=promotion.price)
            db.session.add(order_promotion)

    # Obtener el ID de la dirección de envío seleccionada
    shipping_address_id = request.form.get('shipping_address')

    if shipping_address_id:
        new_order.shipping_address_id = shipping_address_id  # Asociar la dirección seleccionada
    else:
        # Crear una nueva dirección si no se seleccionó una
        new_address_line_1 = request.form.get('new_address_line_1')
        new_city = request.form.get('new_city')
        new_postal_code = request.form.get('new_postal_code')
        new_country = request.form.get('new_country')

        new_address = ShippingAddress(
            user_id=user.id,
            address_line_1=new_address_line_1,
            city=new_city,
            postal_code=new_postal_code,
            country=new_country
        )
        db.session.add(new_address)
        db.session.commit()  # Guardar la dirección

        new_order.shipping_address_id = new_address.id  # Asociar la nueva dirección a la orden

    db.session.commit()  # Guardar la relación con la dirección de envío

    # Guardar el historial de compras
    purchase_history = PurchaseHistory(user_id=user.id, order_id=new_order.id)
    db.session.add(purchase_history)
    db.session.commit()

    # Webhook: notificar compra exitosa
    webhook_url = "https://webhook-test.com/1c8b8262c234f641a7490c73b17b10cf"  # Cambiar a la URL del webhook real
    payload = {
        "event": "purchase_completed",
        "data": {
            "order_id": new_order.id,
            "user_id": user.id,
            "total_price": total_price,
            "payment_method": payment_method.name,
            "status": new_order.status,
            "shipping_address": {
                "line_1": new_address.address_line_1,
                "city": new_address.city,
                "postal_code": new_address.postal_code,
                "country": new_address.country
            }
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

    # Redirigir a una página de confirmación
    flash("¡Compra realizada exitosamente!", "success")
    return redirect(url_for('views.index', order_id=new_order.id))

# Rutas para la ubicación del repartidor
ubicacion_repartidor = {"lat": None, "lon": None}


@views_blueprint.route('/obtener_ubicacion', methods=['GET'])
def obtener_ubicacion():
    """Devuelve la ubicación actual del repartidor"""
    if ubicacion_repartidor["lat"] is not None and ubicacion_repartidor["lon"] is not None:
        return jsonify({"ubicacion": ubicacion_repartidor})
    else:
        return jsonify({"mensaje": "Ubicación no disponible"}), 404


# Url de Footer
@views_blueprint.route('/acerca')
def acerca():
    return render_template('footer_page/acerca.html')  # Ruta correcta a acerca.html

@views_blueprint.route('/mision')
def mision():
    return render_template('footer_page/mision.html')  # Ruta correcta a mision.html

@views_blueprint.route('/vision')
def vision():
    return render_template('footer_page/vision.html')  # Ruta correcta a vision.html

@views_blueprint.route('/terminos')
def terminos():
    return render_template('footer_page/terminos.html')  # Ruta correcta a terminos.html

@views_blueprint.route('/contactanos')
def contactanos():
    return render_template('footer_page/contactanos.html')  # Ruta correcta a contactanos.html

@views_blueprint.route('/politicas')
def politicas():
    return render_template('footer_page/politicas.html')  # Ruta correcta a politicas.html

@views_blueprint.route('/libro')
def libro():
    return render_template('footer_page/libro.html')  # Ruta correcta a libro.html




@views_blueprint.route('/rastreo')
def rastreo():
    """Página para el repartidor que envía la ubicación en tiempo real"""
    return render_template('rastreo.html')
