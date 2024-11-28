from app import create_app, db
from app.models import Pizza, Category

# Función para insertar las pizzas
def insert_pizzas_data():
    # Datos de las pizzas: (name, description, price, image, category_id)
    pizzas_data = [
        ('Mozarrella', 'Doble Queso de mozzarella y Salsa de Tomate', 19.90, 'images/clasicas1.webp', 6),
        ('Vegetariana', 'Queso Mozzarella, Salsa de Tomate, Cebolla, champiñones, Pimiento, Aceitunas y Tomates', 19.90, 'images/clasicas2.webp', 6),
        ('Pepperoni', 'Queso Mozarella, Pepperoni y Salsa de Tomate', 19.90, 'images/clasicas3.webp', 6),
        ('Americana', 'Queso mozzarella, salsa de tomate y Jamón americano', 19.90, 'images/clasicas4.webp', 6),
        ('Española', 'Queso mozarella, Salsa de mantequilla y ajo, Chorizo, Cebolla, y Aceitunas', 23.90, 'images/especialidad1.webp', 5),
        ('Súper Margarita 6 Quesos', '6 Quesos, Salsa de Tomate, Orégano y Tomate', 23.90, 'images/especialidad2.webp', 5),
        ('Continentalle', 'Queso Mozzarella, Jamón, Salsa de Tomate, Champiñones y Cebolla', 23.90, 'images/especialidad3.webp', 5),
        ('Hawaiana', 'Queso mozzarella, salsa de tomate especial, Jamón y Piña', 23.90, 'images/especialidad4.webp', 5)
    ]

    # Insertar las pizzas
    for pizza in pizzas_data:
        name, description, price, image, category_id = pizza

        # Buscar la categoría por su ID
        category = Category.query.filter_by(id=category_id).first()

        if not category:
            print(f"Error: No se encontró la categoría con ID '{category_id}' para la pizza '{name}'.")
            continue

        # Verificar si la pizza ya existe
        existing_pizza = Pizza.query.filter_by(name=name).first()
        if existing_pizza:
            print(f"La pizza '{name}' ya existe.")
            continue

        # Crear y agregar la pizza
        new_pizza = Pizza(
            name=name,
            description=description,
            price=price,
            image=image,
            category_id=category.id
        )
        db.session.add(new_pizza)

    # Confirmar los cambios en la base de datos
    db.session.commit()
    print("Pizzas insertadas con éxito.")

if __name__ == "__main__":
    app = create_app()  # Crear la aplicación Flask
    with app.app_context():  # Usar el contexto de la aplicación
        insert_pizzas_data()
