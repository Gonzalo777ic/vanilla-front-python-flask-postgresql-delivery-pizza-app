from flask import Flask, request, jsonify, render_template

app = Flask(__name__, static_folder='static')
# Datos de promociones
promotions_data = {
    "5mas": [
        {
            'title': 'Martes Pidete Dúo Familiar',
            'description': '2 Pizzas Familiares Clásicas con 1 Gaseosa 1.5L.',
            'price': 'S/ 52.90',
            'image': 'images/cinco1.webp'
        },
        {
            'title': 'Superpack Familiar',
            'description': '4 Pizzas familiares; ideal para 5-6 personas por pizza',
            'price': 'S/ 109.90',
            'image': 'images/cinco2.webp'
        },
        {
            'title': 'Triple Pack Familiar',
            'description': '3 Pizzas Familiares clásicas con 6 pepperoni rolls',
            'price': 'S/ 89.90',
            'image': 'images/cinco3.webp'
        },
        {
            'title': 'Tripack',
            'description': '3 pizzas grandes cualquier sabor con un complemento + 1 Gaseosa de 1.5 LT',
            'price': 'S/ 79.90',
            'image': 'images/cinco4.webp'
        }
    ],
    "cuatropersonas": [
        {
            'title': 'Dúo Familiar',
            'description': '2 pizzas familiares clásicas, masa artesanal y queso 100% mozzarella',
            'price': 'S/ 49.90',
            'image': 'images/cuatro1.webp'
        },
        {
            'title': 'Dúo Grande',
            'description': '2 pizzas grandes clásicas, masa artesanal y queso 100% mozzarella',
            'price': 'S/ 29.90',
            'image': 'images/cuatro2.webp'
        },
        {
            'title': 'Combo Full',
            'description': '1 pizza grande cualquier sabor con 6 alitas o 8 rolls de manjar + 1 Gaseosa de 1 LT',
            'price': 'S/ 39.90',
            'image': 'images/cuatro3.webp'
        },
        {
            'title': 'Pizza Grande',
            'description': '2 pizzas grandes cualquier sabor con un complemento + 1 Gaseosa de 1 LT',
            'price': 'S/ 45.90',
            'image': 'images/cuatro4.webp'
        }
    ],
    "dospersonas": [
        {
            'title': 'Familiar Clásica',
            'description': '1 pizza familiar clásica con 3 rolls de pepperoni',
            'price': 'S/ 33.90',
            'image': 'images/dos1.webp'
        },
        {
            'title': 'Dúo Clásica',
            'description': '2 Pizzas clásicas personales con 2 gaseosas de 500ml',
            'price': 'S/ 19.90',
            'image': 'images/dos2.webp'
        },
        {
            'title': 'Grande Clásica',
            'description': '1 pizza grande clásica o especialidad con 3 rolls de pepperoni',
            'price': 'S/ 39.90',
            'image': 'images/dos3.webp'
        },
        {
            'title': 'Combinación Clásica',
            'description': '1 pizza grande clásica con 1 gaseosa y 3 rolls de pepperoni',
            'price': 'S/ 29.90',
            'image': 'images/dos4.webp'
        },
        {
            'title': 'Pizza grande',
            'description': '1 pizza grande clásica con 1 gaseosa 1LT, masa artesanal y queso 100% mozzarella',
            'price': 'S/ 25.90',
            'image': 'images/dos5.webp'
        }
    ],
    "unapersona": [
        {
            'title': 'Combo Mediano Full',
            'description': '1 Pizza mediana clásica con 3 rolls de pepperoni y gaseosa',
            'price': 'S/ 20.90',
            'image': 'images/personal.webp'
        },
        {
            'title': 'Combo Personal Full',
            'description': 'Pizza personal clásica con 3 rolls de pepperoni y gaseosa',
            'price': 'S/ 15.90',
            'image': 'images/personalFull.webp'
        },
        {
            'title': 'Combo Personal Clásico',
            'description': '1 Pizza clásica personal con 1 gaseosa de 500ml',
            'price': 'S/ 10.90',
            'image': 'images/personalclasico.webp'
        }
    ]
}


@app.route('/')
@app.route('/promociones/promociones')
def promociones():
    """Mostrar todas las promociones"""
    all_promotions = []
    for category in promotions_data.values():
        all_promotions.extend(category)
    return render_template('promociones/promociones.html', promotions=all_promotions)

# Plantillas
@app.route('/miPlantilla')
def layout():
    """Página principal para visualizar promociones y la ubicación del repartidor"""
    return render_template('layout.html')

@app.route('/navbar')
def navbar():
    """Página principal para visualizar promociones y la ubicación del repartidor"""
    return render_template('navbar.html')


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
    return render_template('index.html', promotions_data=promotions_data)

@app.route('/rastreo')
def rastreo():
    """Página para el repartidor que envía la ubicación en tiempo real"""
    return render_template('rastreo.html')

@app.route('/search')
def search():
    query = request.args.get('query', '').strip().lower()
    resultados = []

    if query:  # Si hay una consulta de búsqueda
        # Combinar todas las promociones en una lista
        all_promotions = [promo for category in promotions_data.values() for promo in category]

        # Filtrar las promociones que coincidan con la consulta
        resultados = [
            promo for promo in all_promotions
            if query in promo['title'].lower() or query in promo['description'].lower()
        ]

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
