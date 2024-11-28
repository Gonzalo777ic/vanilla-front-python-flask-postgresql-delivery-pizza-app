from datetime import datetime
from . import db
from flask_login import UserMixin
import bcrypt  # Importamos bcrypt


# Tu clase Users, añades la herencia de UserMixin para que Flask-Login pueda manejar el login.
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Método para establecer la contraseña de manera segura
    def set_password(self, password):
        # Generar un hash con bcrypt
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Método para verificar la contraseña
    def check_password(self, password):
        # Verificar si la contraseña proporcionada coincide con el hash almacenado
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    # Relación con promociones (uno a muchos)
    promotions = db.relationship('Promotion', backref='category_relationship', lazy=True)

class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    category_type = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

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
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    users = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    pizza = db.relationship('Pizza', backref=db.backref('cart_items', lazy=True))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    users = db.relationship('User', backref=db.backref('orders', lazy=True))
    pizzas = db.relationship('Pizza', secondary='order_pizza', backref=db.backref('orders', lazy='dynamic'))

class OrderPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

class PaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=True)

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
