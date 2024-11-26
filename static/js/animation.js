window.onload = function () {
    // Comprobar si es la primera carga de la página en la sesión
    if (!sessionStorage.getItem("hasLoaded")) {
        const loadingScreen = document.getElementById("loading-screen");

        // Inicia la animación de desvanecimiento después de 3 segundos
        setTimeout(function () {
            loadingScreen.style.opacity = "0";

            // Desactivar la interacción inmediatamente durante el desvanecimiento
            loadingScreen.style.pointerEvents = "none";

            // Después de 1.5 segundos, ocultar completamente el elemento
            setTimeout(function () {
                loadingScreen.style.display = "none";
                sessionStorage.setItem("hasLoaded", "true"); // Guardar en sessionStorage
            }, 3000); // Duración del desvanecimiento
        }, 0); // Tiempo antes de iniciar el desvanecimiento
    } else {
        // Si ya se ha mostrado antes, ocultar la pantalla de carga inmediatamente
        document.getElementById("loading-screen").style.display = "none";
    }
};
