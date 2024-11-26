from flask import Flask, request, jsonify, render_template

app = Flask(__name__, static_folder='static')

IMAGE_PATH = 'images/'


# Base de datos simulada para almacenar la ubicación del repartidor
ubicacion_repartidor = {"lat": None, "lon": None}



# Datos de promociones
promotions_data = {
    "5mas": [
        {
            'title': 'Martes Pidete Dúo Familiar',
            'description': '2 Pizzas Familiares Clásicas con 1 Gaseosa 1.5L.',
            'price': 'S/ 52.90',
            'image': 'cinco1.webp'
        },
        {
            'title': 'Superpack Familiar',
            'description': '4 Pizzas familiares; ideal para 5-6 personas por pizza',
            'price': 'S/ 109.90',
            'image': 'cinco2.webp'
        },
        # Más promociones...
    ],
    "cuatropersonas": [
        # Definir las promociones para 3-4 personas
    ],
    # Otras categorías de promociones...
}

@app.route('/promotions')
def promotions():
    # Aquí usamos la variable `promotions_data`
    return render_template('promociones/promociones.html', promotions=promotions_data)

@app.route('/')
def layout():
    """Página principal para visualizar promociones y la ubicación del repartidor"""
    return render_template('layout.html')

@app.route('/promociones')
def promociones():
    """Página de promociones, se puede personalizar para mostrar una categoría específica"""
    category = request.args.get('category', '5mas')  # Usamos un parámetro para elegir la categoría
    promotions = promotions_data.get(category, [])
    return render_template('promociones.html', promotions=promotions)

@app.route('/promociones/promociones')
def vertodo():
    """Mostrar todas las promociones"""
    all_promotions = []
    for category in promotions_data.values():
        all_promotions.extend(category)
    return render_template('promociones/promociones.html', promotions=all_promotions)

@app.route('/pizzas/todo')
def todo():
    return render_template('pizzas/todo.html', filter="5amas")

@app.route('/pizzas/clasicas')
def clasicas():
    return render_template('pizzas/clasicas.html', filter="5amas")

@app.route('/pizzas/especialidades')
def especialidades():
    return render_template('pizzas/especialidades.html', filter="5amas")

@app.route('/combos/todos')
def todos():
    return render_template('combos/todos.html', filter="5amas")

@app.route('/contactanos')
def contactanos():
    """Página para contacto"""
    return render_template('contactanos.html')

@app.route('/index')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/rastreo')
def rastreo():
    """Página para el repartidor que envía la ubicación en tiempo real"""
    return render_template('rastreo.html')

@app.route('/search')
def search():
    query = request.args.get('query', '')
    resultados = []  # Cambia esta línea con tu lógica de búsqueda.
    return render_template('search.html', query=query, resultados=resultados)

@app.route('/actualizar_ubicacion', methods=['POST'])
def actualizar_ubicacion():
    """Recibe la ubicación actual del repartidor desde el móvil"""
    data = request.get_json()
    lat = data.get("lat")
    lon = data.get("lon")

    # Actualiza la ubicación en la memoria
    ubicacion_repartidor["lat"] = lat
    ubicacion_repartidor["lon"] = lon

    return jsonify({"mensaje": "Ubicación actualizada correctamente"}), 200

@app.route('/obtener_ubicacion', methods=['GET'])
def obtener_ubicacion():
    """Devuelve la ubicación actual del repartidor"""
    if ubicacion_repartidor["lat"] is not None and ubicacion_repartidor["lon"] is not None:
        return jsonify({"ubicacion": ubicacion_repartidor})
    else:
        return jsonify({"mensaje": "Ubicación no disponible"}), 404

if __name__ == '__main__':
    app.run(debug=True)
