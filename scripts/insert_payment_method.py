from app import create_app, db
from app.models import PaymentMethod

# Crear la aplicación para acceder a la base de datos
app = create_app()

def insert_payment_methods():
    # Lista de métodos de pago que deseas agregar
    payment_methods = [
        {"name": "Efectivo", "description": "Pago en efectivo al momento de la entrega."},
        {"name": "Tarjeta", "description": "Pago con tarjeta de crédito o débito."},
        {"name": "Yape", "description": "Pago mediante la aplicación Yape."}
    ]
    
    for payment_method_data in payment_methods:
        # Verifica si el método de pago ya existe en la base de datos
        if not PaymentMethod.query.filter_by(name=payment_method_data["name"]).first():
            # Si no existe, lo crea
            payment_method_instance = PaymentMethod(
                name=payment_method_data["name"],
                description=payment_method_data["description"]
            )
            db.session.add(payment_method_instance)
            print(f"Método de pago '{payment_method_data['name']}' insertado correctamente.")
        else:
            print(f"Método de pago '{payment_method_data['name']}' ya existe.")
    
    db.session.commit()  # Confirma los cambios

if __name__ == "__main__":
    with app.app_context():  # Usar el contexto de la aplicación
        insert_payment_methods()
