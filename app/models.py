from datetime import datetime
from . import db
from flask_login import UserMixin
import bcrypt  # Importamos bcrypt
from werkzeug.security import generate_password_hash, check_password_hash


# Tu clase Users, añades la herencia de UserMixin para que Flask-Login pueda manejar el login.
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)  # Nombre
    last_name = db.Column(db.String(120), nullable=False)   # Apellidos
    document_type = db.Column(db.String(50), nullable=False)  # Tipo de Documento (DNI o Pasaporte)
    document_number = db.Column(db.String(50), unique=True, nullable=False)  # Número de Documento
    phone_number = db.Column(db.String(15), nullable=False)  # Número de Teléfono
    email = db.Column(db.String(120), unique=True, nullable=False)  # Correo Electrónico
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nombre de usuario generado
    password = db.Column(db.String(255), nullable=False)  # Contraseña

    # Método para establecer la contraseña de manera segura
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_username(self):
        base_username = f"{self.first_name.lower()}.{self.last_name.lower()}"
        base_username = base_username.replace(" ", "")
        counter = 1
        while User.query.filter_by(username=base_username).first():
            base_username = f"{self.first_name.lower()}.{self.last_name.lower()}{counter}"
            counter += 1
        self.username = base_username



class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)  # Título de la promoción
    description = db.Column(db.String(500), nullable=False)  # Descripción de la promoción
    price = db.Column(db.Float, nullable=False)  # Precio de la promoción
    image = db.Column(db.String(255), nullable=False)  # Imagen asociada
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)  # Relación con categorías

    # Relación con Category
    category = db.relationship('Category', backref=db.backref('promotions', lazy=True))


class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    # Cambié el backref para evitar conflictos
    category = db.relationship('Category', backref=db.backref('pizzas', lazy=True))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), nullable=False)

class ShoppingCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=True)  # Pizza puede ser nula si es una promoción
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotion.id'), nullable=True)  # Relación con promociones
    quantity = db.Column(db.Integer, nullable=False, default=1)  # Cantidad de pizza o promoción en el carrito
    users = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    pizza = db.relationship('Pizza', backref=db.backref('cart_items', lazy=True), uselist=False)
    promotion = db.relationship('Promotion', backref=db.backref('cart_items', lazy=True), uselist=False)  # Relación con promoción

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Relación con el usuario
    total_price = db.Column(db.Float, nullable=False)  # Precio total de la orden
    status = db.Column(db.String(50), nullable=False)  # Estado de la orden (ejemplo: Pagado, Pendiente)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha de creación
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_method.id'), nullable=False)  # Método de pago
    users = db.relationship('User', backref=db.backref('orders', lazy=True))
    pizzas = db.relationship('Pizza', secondary='order_pizza', backref=db.backref('orders', lazy='dynamic'))
    promotions = db.relationship('Promotion', secondary='order_promotion', backref=db.backref('orders', lazy='dynamic'))  # Relación con promociones

class OrderPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

class OrderPromotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)  # Relación con Order
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotion.id'), nullable=False)  # Relación con Promotion
    quantity = db.Column(db.Integer, nullable=False, default=1)  # Cantidad de promociones
    price = db.Column(db.Float, nullable=False)  # Precio aplicado de la promoción
    
class PaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)  # Nombre del método de pago (ej. "Tarjeta", "PayPal")
    description = db.Column(db.String(255), nullable=True)  # Descripción opcional
    orders = db.relationship('Order', backref='payment_method', lazy=True)  # Relación con órdenes


class ShippingAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    address_line_1 = db.Column(db.String(255), nullable=False)
    address_line_2 = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(120), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    users = db.relationship('User', backref=db.backref('addresses', lazy=True))

class PurchaseHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    users = db.relationship('User', backref=db.backref('purchase_history', lazy=True))
    order = db.relationship('Order', backref=db.backref('purchase_history', lazy=True))

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    users = db.relationship('User', backref=db.backref('recommendations', lazy=True))
    pizza = db.relationship('Pizza', backref=db.backref('recommendations', lazy=True))

class AppliedPromotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotion.id'), nullable=False)
    order = db.relationship('Order', backref=db.backref('applied_promotions', lazy=True))
    promotion = db.relationship('Promotion', backref=db.backref('applied_promotions', lazy=True))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), nullable=True)
    users = db.relationship('User', backref=db.backref('reviews', lazy=True))
    pizza = db.relationship('Pizza', backref=db.backref('reviews', lazy=True))
