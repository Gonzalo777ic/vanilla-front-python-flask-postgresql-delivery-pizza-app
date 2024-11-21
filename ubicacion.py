from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Base de datos simulada para almacenar la ubicación del repartidor
ubicacion_repartidor = {"lat": None, "lon": None}


@app.route('/')
def layout():
    """Página principal para visualizar promociones y la ubicación del repartidor"""
    return render_template('layout.html')



@app.route('/promociones/vertodo')
def vertodo():
    return render_template('promociones/vertodo.html', filter="todo")

@app.route('/promociones/unapersona')
def unapersona():
    return render_template('promociones/unapersona.html', filter="1persona")

@app.route('/promociones/dospersonas')
def dospersonas():
    return render_template('promociones/dospersonas.html', filter="2personas")

@app.route('/promociones/cuatropersonas')
def cuatropersonas():
    return render_template('promociones/cuatropersonas.html', filter="3-4personas")

@app.route('/promociones/cincoamas')
def cincoamas():
    return render_template('promociones/cincoamas.html', filter="5amas")



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
@app.route('/combos/dos')
def dos():
    return render_template('combos/dos.html', filter="5amas")
@app.route('/combos/cuatro')
def cuatro():
    return render_template('combos/cuatro.html', filter="5amas")



@app.route('/contactanos')
def contactanos():
    """Página principal para visualizar promociones y la ubicación del repartidor"""
    return render_template('contactanos.html')

@app.route('/index')
def index():
    """Página principal para visualizar promociones y la ubicación del repartidor"""
    return render_template('index.html')

@app.route('/rastreo')
def rastreo():
    """Página para el repartidor que envía la ubicación en tiempo real"""
    return render_template('rastreo.html')

@app.route('/search')
def search():
    query = request.args.get('query', '')
    # Simulación de resultados vacíos para este ejemplo
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
    