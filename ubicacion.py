from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Base de datos simulada para almacenar la ubicación del repartidor
ubicacion_repartidor = {"lat": None, "lon": None}


@app.route('/')
def layout():
    """Página principal para visualizar promociones y la ubicación del repartidor"""
    return render_template('layout.html')

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

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    # Lógica para manejar la búsqueda
    return f"Resultados de búsqueda para: {query}"


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
