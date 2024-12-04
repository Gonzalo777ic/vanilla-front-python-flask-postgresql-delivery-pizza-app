from app import create_app, db
from app.models import Promotion, Category

# Función para insertar las promociones
def insert_promotions_data():
    # Datos de las promociones
    promotions_data = [
        # (title, description, price, image, category_name)
        ('Martes Pidete Dúo Familiar', '2 Pizzas Familiares Clásicas con 1 Gaseosa 1.5L.', 52.9, 'images/cinco1.webp', 1),
        ('Superpack Familiar', '4 Pizzas familiares; ideal para 5-6 personas por pizza', 109.9, 'images/cinco2.webp', 1),
        ('Triple Pack Familiar', '3 Pizzas Familiares clásicas con 6 pepperoni rolls', 89.9, 'images/cinco3.webp', 1),
        ('Tripack', '3 pizzas grandes cualquier sabor con un complemento + 1 Gaseosa de 1.5 LT', 79.9, 'images/cinco4.webp', 1),
        ('Dúo Familiar', '2 pizzas familiares clásicas, masa artesanal y queso 100% mozzarella', 49.9, 'images/cuatro1.webp', 2),
        ('Dúo Grande', '2 pizzas grandes clásicas, masa artesanal y queso 100% mozzarella', 29.9, 'images/cuatro2.webp', 2),
        ('Combo Full', '1 pizza grande cualquier sabor con 6 alitas o 8 rolls de manjar + 1 Gaseosa de 1 LT', 39.9, 'images/cuatro3.webp', 2),
        ('Pizza Grande', '2 pizzas grandes cualquier sabor con un complemento + 1 Gaseosa de 1 LT', 45.9, 'images/cuatro4.webp', 2),
        ('Familiar Clásica', '1 pizza familiar clásica con 3 rolls de pepperoni', 33.9, 'images/dos1.webp', 3),
        ('Dúo Clásica', '2 Pizzas clásicas personales con 2 gaseosas de 500ml', 19.9, 'images/dos2.webp', 3),
        ('Grande Clásica', '1 pizza grande clásica o especialidad con 3 rolls de pepperoni', 39.9, 'images/dos3.webp', 3),
        ('Combinación Clásica', '1 pizza grande clásica con 1 gaseosa y 3 rolls de pepperoni', 29.9, 'images/dos4.webp', 3),
        ('Pizza grande', '1 pizza grande clásica con 1 gaseosa 1LT, masa artesanal y queso 100% mozzarella', 25.9, 'images/dos5.webp', 3),
        ('Combo Mediano Full', '1 Pizza mediana clásica con 3 rolls de pepperoni y gaseosa', 20.9, 'images/personal.webp', 4),
        ('Combo Personal Full', 'Pizza personal clásica con 3 rolls de pepperoni y gaseosa', 15.9, 'images/personalFull.webp', 4),
        ('Combo Personal Clásico', '1 Pizza clásica personal con 1 gaseosa de 500ml', 10.9, 'images/personalclasico.webp', 4)
    ]

    # Insertar las promociones
    for promotion in promotions_data:
        title, description, price, image, category_id = promotion

        # Buscar la categoría por su nombre
        category = Category.query.filter_by(id=category_id).first()

        if not category:
            print(f"Error: No se encontró la categoría '{category_id}' para la promoción '{title}'.")
            continue

        # Verificar si la promoción ya existe
        existing_promotion = Promotion.query.filter_by(title=title).first()
        if existing_promotion:
            print(f"La promoción '{title}' ya existe.")
            continue

        # Crear y agregar la promoción
        new_promotion = Promotion(
            title=title,
            description=description,
            price=price,
            image=image,
            category_id=category.id
        )
        db.session.add(new_promotion)

    # Confirmar los cambios en la base de datos
    db.session.commit()
    print("Promociones insertadas con éxito.")

if __name__ == "__main__":
    app = create_app()  # Crear la aplicación Flask
    with app.app_context():  # Usar el contexto de la aplicación
        insert_promotions_data()
