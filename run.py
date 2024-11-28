from app import create_app

# Crea la aplicación con la función que ya define toda la configuración
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
