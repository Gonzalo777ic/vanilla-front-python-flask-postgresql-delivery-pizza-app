document.addEventListener('DOMContentLoaded', function () {
    const filterButtons = document.querySelectorAll('.filter');
    const promotions = document.querySelectorAll('.promotion');
    
    // Función para mostrar todas las promociones
    function mostrarTodo() {
        promotions.forEach(promotion => {
            promotion.style.display = 'block';
        });
    }

    // Función para filtrar por categoría
    function filtrarPromociones(categoria) {
        promotions.forEach(promotion => {
            if (promotion.dataset.category === categoria || categoria === 'todo') {
                promotion.style.display = 'block';
            } else {
                promotion.style.display = 'none';
            }
        });
    }

    // Asociar los botones a sus funciones
    filterButtons.forEach(button => {
        button.addEventListener('click', function () {
            const categoria = this.id.replace('Button', ''); // 'verTodoButton' -> 'verTodo'
            if (categoria === 'verTodo') {
                mostrarTodo();
            } else {
                filtrarPromociones(categoria);
            }
        });
    });

    // Mostrar todas las promociones al cargar la página
    mostrarTodo();
});
