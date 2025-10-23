// Efecto del Banner //
$('.hero-slider').slick({
  dots: false,
  infinite: true,
  speed: 300,
  slidesToShow: 1,
  slidesToScroll: 1,
  autoplay: true,
  autoplaySpeed: 2000,
  arrows: false,
});

// Efecto de las categorias //
$('.slider-category').slick({
  dots: false,
  infinite: true,
  speed: 300,
  slidesToShow: 6,
  slidesToScroll: 1,
  autoplay: true,
  autoplaySpeed: 2000,
  arrows: false,
  draggable: true,
  swipeToSlide: true,
});

// Efecto Parallax //
document.addEventListener("DOMContentLoaded", function () {
  const verifier = document.getElementById("age-verifier");
  const imgs = document.querySelectorAll("#parallax-container img");

  if (verifier && imgs.length) {
    verifier.addEventListener("scroll", () => {
      let st = verifier.scrollTop;

      imgs.forEach((img, index) => {
        // velocidades distintas según la capa
        let speedsY = [-0.1, 0.6, -0.2, 0.1];
        let speedsX = [0, -0.4, 0, 0]
        let speedY = speedsY[index] !== undefined ? speedsY[index] : 0.5;
        let speedX = speedsX[index] !== undefined ? speedsX[index] : 0;
        img.style.transform = `translate(${st * speedX}px, ${st * speedY}px)`;
      });
    });
  }
});

// Ocultar Pagina Principal y efecto del boton de mayores de 18 años//
$(document).ready(function () {
  $('#verify-button').on('click', function () {
    $('#age-verifier').fadeOut(800, function () {
      $('body').css({ 'overflow': 'auto', 'height': 'auto' });
      $('#main-site-content').fadeIn(800);
    });
  });

  // Efecto de "Emergencia" del Botón 
  setTimeout(function () {
    $('#verify-button').addClass('is-visible');
  }, 2000);
});

// Recalcular contenido principal despues del bloqueo//
document.getElementById("verify-button").addEventListener("click", () => {
  const verifier = document.getElementById("age-verifier");
  verifier.style.display = "none";

  // Forzar reflow
  setTimeout(() => {
    window.dispatchEvent(new Event("resize"));
    document.body.offsetHeight;
  }, 50);
});
// Desvanecer el Header//
window.addEventListener("load", () => {
  document.querySelector("header").classList.add("loaded");
});

// Efecto de nieve //
const TOTAL_SNOWFLAKES = 20;
const snowContainer = document.querySelector('.hero-sec .snow-container');

function createSnowflake() {
  const snowflake = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  snowflake.classList.add("snowflake");
  snowflake.setAttribute("viewBox", "0 0 24 24");
  snowflake.innerHTML = `<path fill="white" d="M12 2L13 8H17L14 10L15 16L12 14L9 16L10 10L7 8H11L12 2Z"/>`;

  snowflake.style.left = Math.random() * 100 + "%";
  snowflake.style.animationDuration = 5 + Math.random() * 5 + "s";
  snowflake.style.animationDelay = Math.random() * 5 + "s";

  snowContainer.appendChild(snowflake);

  snowflake.addEventListener("animationend", () => {
    snowflake.remove();
    createSnowflake();
  });
}

for (let i = 0; i < TOTAL_SNOWFLAKES; i++) {
  setTimeout(createSnowflake, i * 200);
}


