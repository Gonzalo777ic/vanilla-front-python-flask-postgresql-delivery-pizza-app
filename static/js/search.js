document.addEventListener("DOMContentLoaded", () => {
    const searchForm = document.getElementById("search-form");
    const searchInput = document.getElementById("search-input");
    const resultsContainer = document.getElementById("results-container");

    // Simulación de datos para búsqueda (esto debería venir del servidor en producción)
    const promotions = [
        { id: 1, name: "Combo Familiar", description: "2 pizzas grandes + gaseosa", price: "S/49.90", image: "images/combo2.webp" },
        { id: 2, name: "Pizza Clásica", description: "Pizza mediana clásica", price: "S/29.90", image: "images/clasicas1.webp" },
        { id: 3, name: "Combo Personal", description: "1 pizza personal + gaseosa", price: "S/19.90", image: "images/personal.webp" }
    ];

    // Manejar el evento de envío del formulario
    searchForm.addEventListener("submit", (event) => {
        event.preventDefault(); // Evitar recargar la página
        const query = searchInput.value.trim().toLowerCase();

        if (query) {
            const filteredResults = promotions.filter(promotion =>
                promotion.name.toLowerCase().includes(query) ||
                promotion.description.toLowerCase().includes(query)
            );

            // Priorizar los resultados con coincidencias en el nombre (título)
            const prioritizedResults = filteredResults.sort((a, b) => {
                const aInTitle = a.name.toLowerCase().includes(query) ? 1 : 0;
                const bInTitle = b.name.toLowerCase().includes(query) ? 1 : 0;
                return bInTitle - aInTitle; // Ordenar primero por coincidencias en el título
            });

            renderResults(prioritizedResults);
        } else {
            renderResults([]); // No hay resultados si la búsqueda está vacía
        }
    });

    // Función para renderizar resultados en el contenedor
    function renderResults(results) {
        if (results.length > 0) {
            resultsContainer.innerHTML = results.map(result => `
                <div class="promotion">
                    <img src="${result.image}" alt="${result.name}" class="promotion-image">
                    <h2>${result.name}</h2>
                    <p>${result.description}</p>
                    <p class="price">${result.price}</p>
                    <button>COMPRAR</button>
                </div>
            `).join('');
        } else {
            resultsContainer.innerHTML = `
                <div class="alert alert-info">
                    <i class="icon">ℹ️</i> No encontramos productos que coincidan con tu búsqueda.
                </div>
                <div class="no-results">
                    <img src="images/noresultado.png" alt="Sin resultados" class="no-results-image">
                    <h2>NO SE HAN ENCONTRADO RESULTADOS</h2>
                    <p class="suggestions-title">Sugerencia de búsqueda</p>
                    <ul class="suggestions-list">
                        <li>Revisa la ortografía de las palabras.</li>
                        <li>Usa términos más generales.</li>
                    </ul>
                    <a href="/" class="home-button">IR AL MENÚ</a>
                </div>
            `;
        }
    }
});
