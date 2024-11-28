from flask import Flask, Blueprint, request, jsonify, render_template
from .models import Category, Promotion, Pizza
from . import db

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

@views_blueprint.route('/search')
def search():
    query = request.args.get('query', '').strip().lower()  # Obtener la consulta de búsqueda
    resultados = []

    if query:
        # Filtrar directamente desde la base de datos usando LIKE para que la búsqueda sea eficiente
        resultados = Promotion.query.filter(
            (Promotion.title.ilike(f"%{query}%")) | 
            (Promotion.description.ilike(f"%{query}%"))
        ).all()

    return render_template('search.html', query=query, resultados=resultados)

@views_blueprint.route('/pizzas/pizzas', methods=['GET'])
def mostrar_pizzas():
    category = request.args.get('category')  # Obtiene la categoría de la URL
    if category:
        pizzas = Pizza.query.filter_by(category_id=category).all()
    else:
        pizzas = Pizza.query.all()  # Muestra todas si no hay filtro
    return render_template('pizzas/pizzas.html', pizzas=pizzas)



@views_blueprint.route('/combos/todos')
def todos():
    return render_template('combos/todos.html', filter="5amas")

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


