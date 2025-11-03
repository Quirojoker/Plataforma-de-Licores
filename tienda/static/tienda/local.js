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

// Recalcular contenido principal despues del bloqueo
document.addEventListener('DOMContentLoaded', function() {
    const verifyButton = document.getElementById("verify-button");
    
    // VERIFICAR que el botón existe antes de agregar el evento
    if (verifyButton) {
        verifyButton.addEventListener("click", () => {
            const verifier = document.getElementById("age-verifier");
            if (verifier) {
                verifier.style.display = "none";

                // Forzar reflow
                setTimeout(() => {
                    window.dispatchEvent(new Event("resize"));
                    document.body.offsetHeight;
                }, 50);
            }
        });
    }
});

// Desvanecer el Header//
window.addEventListener("load", () => {
  document.querySelector("header").classList.add("loaded");
});

// Efecto de nieve //
const TOTAL_SNOWFLAKES = 50;
const snowContainer = document.querySelector('.hero-sec .snow-container');

// VERIFICAR que el contenedor de nieve existe
if (snowContainer) {
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
}

// Web share API //
function shareProduct() {
    if (navigator.share) {
        navigator.share({
            title:'Valhalla - ' + document.title,
            text: '¡Mira este producto increíble!', 
            url: window.location.href 
        })
        .then(() => console.log('Compartido exitosamente'))
        .catch((error) => console.log('Error al compartir:', error));
    } else {
        
        alert('Tu navegador no soporta la función de compartir nativa');
    }
}

// Selector de Cantidad //
function increaseQuantity() {
    const input = document.getElementById('quantity-input');
    let value = parseInt(input.value) || 0;
    input.value = value + 1;
}

function decreaseQuantity() {
    const input = document.getElementById('quantity-input');
    if (parseInt(input.value) > 1) {
        input.value = parseInt(input.value) - 1;
    }
}


// Efecto de scroll en imágenes del producto
document.addEventListener('DOMContentLoaded', function() {
    const scrollContainer = document.querySelector('.scroll-container');
    const productSection = document.querySelector('section'); // La sección de detalle
    
    if (scrollContainer && productSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const sectionTop = productSection.offsetTop;
            const sectionBottom = sectionTop + productSection.offsetHeight;
            
            // Solo aplicar efecto si estamos DENTRO de la sección
            if (scrolled >= sectionTop && scrolled <= sectionBottom - window.innerHeight) {
                const movement = (scrolled - sectionTop) * 1.2; // Relativo al inicio de la sección
                scrollContainer.style.transform = `translateY(${movement}px)`;
            } else if (scrolled < sectionTop) {
                // Antes de la sección - resetear
                scrollContainer.style.transform = `translateY(0px)`;
            } else {
                // Después de la sección - mantener última posición
                const maxMovement = (sectionBottom - sectionTop - window.innerHeight) * 1.2;
                scrollContainer.style.transform = `translateY(${maxMovement}px)`;
            }
        });
    }
});

