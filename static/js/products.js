document.addEventListener('DOMContentLoaded', function () {
    // Agregar evento de filtrado
    const filterButtons = document.querySelectorAll('.filter');
    filterButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            // Lógica para actualizar promociones con base en el filtro
            getPromotions(button.textContent.toLowerCase().replace(/\s+/g, ''));
        });
    });


    // Cargar promociones de manera dinámica (usando una lista de objetos, por ejemplo)
    const promotionsData = {
        "5mas": [
            {
                title: 'Martes Pidete Dúo Familiar',
                description: '2 Pizzas Familiares Clásicas con 1 Gaseosa 1.5L.',
                price: 'S/ 52.90PICHULAS',
                image: 'images/cinco1.webp'
            },
            {
                title: 'Superpack Familiar',
                description: '4 Pizzas familiares; ideal para 5-6 personas por pizza',
                price: 'S/ 109.90',
                image: 'cinco2.webp'
            },
            {
                title: 'Triple Pack Familiar',
                description: '3 Pizzas Familiares clásicas con 6 pepperoni rolls',
                price: 'S/ 89.90',
                image: 'cinco3.webp'
            },
            {
                title: 'Tripack',
                description: '3 pizzas grandes cualquier sabor con un complemento + 1 Gaseosa de 1.5 LT',
                price: 'S/ 79.90',
                image: 'cinco4.webp'
            }
        ],
        "cuatropersonas": [
            {
                title: 'Dúo Familiar',
                description: '2 pizzas familiares clásicas, masa artesanal y queso 100% mozzarella',
                price: 'S/ 49.90',
                image: 'cuatro1.webp'
            },
            {
                title: 'Dúo Grande',
                description: '2 pizzas grandes clásicas, masa artesanal y queso 100% mozzarella',
                price: 'S/ 29.90',
                image: 'cuatro2.webp'
            },
            {
                title: 'Combo Full',
                description: '1 pizza grande cualquier sabor con 6 alitas o 8 rolls de manjar + 1 Gaseosa de 1 LT',
                price: 'S/ 39.90',
                image: 'cuatro3.webp'
            },
            {
                title: 'Pizza Grande',
                description: '2 pizzas grandes cualquier sabor con un complemento + 1 Gaseosa de 1 LT',
                price: 'S/ 45.90',
                image: 'cuatro4.webp'
            }
        ],
        "dospersonas": [
            {
                title: 'Familiar Clásica',
                description: '1 pizza familiar clásica con 3 rolls de pepperoni',
                price: 'S/ 33.90',
                image: 'dos1.webp'
            },
            {
                title: 'Dúo Clásica',
                description: '2 Pizzas clásicas personales con 2 gaseosas de 500ml',
                price: 'S/ 19.90',
                image: 'dos2.webp'
            },
            {
                title: 'Grande Clásica',
                description: '1 pizza grande clásica o especialidad con 3 rolls de pepperoni',
                price: 'S/ 39.90',
                image: 'dos3.webp'
            },
            {
                title: 'Combinación Clásica',
                description: '1 pizza grande clásica con 1 gaseosa y 3 rolls de pepperoni',
                price: 'S/ 29.90',
                image: 'dos4.webp'
            },
            {
                title: 'Pizza grande',
                description: '1 pizza grande clásica con 1 gaseosa 1LT, masa artesanal y queso 100% mozzarella',
                price: 'S/ 25.90',
                image: 'dos5.webp'
            }
        ],
        "unapersona": [
            {
                title: 'Combo Mediano Full',
                description: '1 Pizza mediana clásica con 3 rolls de pepperoni y gaseosa',
                price: 'S/ 20.90',
                image: 'personal.webp'
            },
            {
                title: 'Combo Personal Full',
                description: 'Pizza personal clásica con 3 rolls de pepperoni y gaseosa',
                price: 'S/ 15.90',
                image: 'personalFull.webp'
            },
            {
                title: 'Combo Personal Clásico',
                description: '1 Pizza clásica personal con 1 gaseosa de 500ml',
                price: 'S/ 10.90',
                image: 'personalclasico.webp'
            }
        ]
    };
    
    function getPromotions(route) {
        const selectedPromotions = promotionsData[route] || promotionsData['5mas']; // '5mas' es la opción por defecto
        displayPromotions(selectedPromotions);
    }
    
    function displayPromotions(promotions) {
        const container = document.getElementById('promotionsContainer');
        container.innerHTML = ''; // Limpiar el contenedor de promociones

        promotions.forEach(promotion => {
            const promotionElement = document.createElement('div');
            promotionElement.classList.add('promotion');
            promotionElement.innerHTML = `
                <img src="${promotion.image}" alt="${promotion.title}">
                <h3>${promotion.title}</h3>
                <p>${promotion.description}</p>
                <p>Precio: ${promotion.price}</p>
            `;
            container.appendChild(promotionElement);
        });
    }

    document.getElementById('verTodoButton').addEventListener('click', () => {
        // Combinar todas las promociones de las categorías disponibles
        const allPromotions = [
            ...promotionsData['unapersona'],
            ...promotionsData['dospersonas'],
            ...promotionsData['cuatropersonas'],
            ...promotionsData['5mas']
        ];

        // Mostrar todas las promociones combinadas
        displayPromotions(allPromotions);
    });

    // Asociar el resto de botones con sus filtros
    document.getElementById('unapersonaButton').addEventListener('click', () => {
        getPromotions('unapersona');
    });
    document.getElementById('cuatropersonasButton').addEventListener('click', () => {
        getPromotions('cuatropersonas');
    });
    document.getElementById('dospersonasButton').addEventListener('click', () => {
        getPromotions('dospersonas');
    });

    // Función para mostrar todas las promociones
    function mostrarTodo() {
        // Mostrar todas las promociones
        document.querySelectorAll('.promotion').forEach(function(promotion) {
            promotion.style.display = 'block';
        });
    }

    // Asociar la función mostrarTodo al clic del botón "Ver todo"
    verTodoButton.addEventListener('click', mostrarTodo);

    // Aquí podrías agregar otras funciones si quieres filtrar por el tipo de promoción, por ejemplo:
    function filtrarPromociones(tipo) {
        document.querySelectorAll('.promotion').forEach(function(promotion) {
            if (promotion.classList.contains(tipo)) {
                promotion.style.display = 'block';
            } else {
                promotion.style.display = 'none';
            }
        });
    }
    // Llamar a la función mostrarTodo cuando se carga la página
    mostrarTodo();

    
});
