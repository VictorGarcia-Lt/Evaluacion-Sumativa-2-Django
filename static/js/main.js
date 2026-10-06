/* ==========================================================================
   Cine Catálogo — JavaScript propio del proyecto
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {
  // 1. Año dinámico en el pie de página
  var anio = document.getElementById("anio-actual");
  if (anio) {
    anio.textContent = new Date().getFullYear();
  }

  // 2. Sombra en el navbar al hacer scroll
  var navbar = document.getElementById("navbar-principal");
  if (navbar) {
    var aplicarSombra = function () {
      navbar.classList.toggle("is-scrolled", window.scrollY > 10);
    };
    aplicarSombra();
    window.addEventListener("scroll", aplicarSombra, { passive: true });
  }

  // 3. Tooltips de Bootstrap (si los hay en el futuro)
  if (typeof bootstrap !== "undefined" && bootstrap.Tooltip) {
    document
      .querySelectorAll('[data-bs-toggle="tooltip"]')
      .forEach(function (elemento) {
        new bootstrap.Tooltip(elemento);
      });
  }
});
