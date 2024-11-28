from app import create_app, db
from app.models import Promotion, Category

# Crear la aplicación para acceder a la base de datos
app = create_app()
def insert_categories():
    categories = ['5mas', 'cuatropersonas', 'dospersonas', 'unapersona','especialidades','clasicas']
    for category_name in categories:
        # Verifica si la categoría ya existe
        if not Category.query.filter_by(name=category_name).first():
            category_instance = Category(name=category_name)
            db.session.add(category_instance)
            print(f"Categoría '{category_name}' insertada correctamente.")
        else:
            print(f"Categoría '{category_name}' ya existe.")
    
    db.session.commit()  # Confirma los cambios

if __name__ == "__main__":
    with app.app_context():  # Usar el contexto de la aplicación
        insert_categories()