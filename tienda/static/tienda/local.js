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
document.addEventListener('DOMContentLoaded', function () {
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
            title: 'Valhalla - ' + document.title,
            text: '¡Mira este producto increíble!',
            url: window.location.href
        })
            .then(() => console.log('Compartido exitosamente'))
            .catch((error) => console.log('Error al compartir:', error));
    } else {

        alert('Tu navegador no soporta la función de compartir nativa');
    }
}

// Inicializar eventos cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function () {
    console.log('Funciones del carrito cargadas');
});


// VERSIÓN ORIGINAL MEJORADA - Scroll libre y natural
document.addEventListener('DOMContentLoaded', function () {
    const scrollContainer = document.querySelector('.scroll-container');
    const productSection = document.querySelector('#seccion-producto-detalle');

    if (scrollContainer && productSection) {
        // Calcular alturas REALES
        const sectionTop = productSection.offsetTop;
        const sectionHeight = productSection.offsetHeight;
        const windowHeight = window.innerHeight;

        // Cuánto puede bajar la imagen (diferencia entre sección y ventana)
        const maxScrollMovement = sectionHeight - windowHeight;

        window.addEventListener('scroll', function () {
            const scrolled = window.pageYOffset;

            // Scroll RELATIVO dentro de la sección
            const scrollWithinSection = scrolled - sectionTop;

            if (scrollWithinSection >= 0 && scrollWithinSection <= maxScrollMovement) {
                // DENTRO de la sección - movimiento proporcional al scroll real
                const movement = scrollWithinSection * 1.2; // Factor de velocidad
                scrollContainer.style.transform = `translateY(${movement}px)`;

            } else if (scrollWithinSection < 0) {
                // ANTES de la sección - reset
                scrollContainer.style.transform = `translateY(0px)`;

            } else {
                // DESPUÉS de la sección - mantener posición final
                const finalMovement = maxScrollMovement * 1.2;
                scrollContainer.style.transform = `translateY(${finalMovement}px)`;
            }
        });
    }
});




// Token de seguridad //
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Función actualizar cantidad //
function actualizarCantidad(itemId, nuevaCantidad) {
    const csrftoken = getCookie('csrftoken');
    
    // SANITIZAR DATOS
    const sanitizedItemId = itemId.toString().replace(/[^0-9]/g, '');
    const sanitizedCantidad = Math.max(1, Math.min(100, parseInt(nuevaCantidad) || 1));
    
    // VALIDAR DATOS
    if (!sanitizedItemId || sanitizedItemId.length === 0) {
        console.error('ID de producto inválido');
        return;
    }

    fetch('/actualizar-cantidad/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: new URLSearchParams({
            item_id: sanitizedItemId,
            cantidad: sanitizedCantidad.toString()
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            document.getElementById(`subtotal-${itemId}`).textContent = `$${Math.round(data.subtotal_producto)}`;
            document.getElementById('subtotal-general').textContent = `$${Math.round(data.subtotal_carrito)}`;
            document.getElementById('total-general').textContent = `$${Math.round(data.total_carrito)}`;
            console.log('Cantidad actualizada en servidor');
            
        } else {
            console.error('Error del servidor:', data.error);
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error de conexión:', error);
        alert('Error de conexión. Intenta nuevamente.');
    });
}





// Funciones de cantidad //
function increaseQuantity(itemId) {
    const input = document.getElementById(`quantity-input-${itemId}`);
    const maxStock = parseInt(input.getAttribute('max')) || 99;
    
    let value = parseInt(input.value) || 1;
    value = Math.max(1, Math.min(maxStock, value + 1));
    
    input.value = value;
    actualizarCantidad(itemId, value);
}

function decreaseQuantity(itemId) {
    const input = document.getElementById(`quantity-input-${itemId}`);
    
    let value = parseInt(input.value) || 1;
    value = Math.max(1, value - 1);
    
    input.value = value;
    actualizarCantidad(itemId, value);
}


// Función para actualizar el contador del carrito
function actualizarContadorCarrito() {
    fetch('/api/cart-count/')
        .then(response => response.json())
        .then(data => {
            const cartCount = document.getElementById('cart-count');
            if (cartCount) {
                cartCount.textContent = data.count;
                if (data.count === 0) {
                    cartCount.style.display = 'none';
                } else {
                    cartCount.style.display = 'inline';
                }
            }
        });
}

// Ejecutar cuando la página carga
document.addEventListener('DOMContentLoaded', function () {
    actualizarContadorCarrito();
});

// Ejecutar cuando se usa el botón "Atrás" del navegador
window.addEventListener('pageshow', function (event) {
    if (event.persisted) {
        actualizarContadorCarrito();
    }
});



// Modificar las funciones existentes//
function increaseQuantity(itemId) {
    const input = document.getElementById(`quantity-input-${itemId}`);
    const maxStock = parseInt(input.getAttribute('max')) || 99;
    let value = parseInt(input.value) || 1;

    if (value < maxStock) {
        value++;
        input.value = value;
        // ENVIAR AL SERVIDOR
        actualizarCantidad(itemId, value);
    } else {
        // AGREGAR ESTA ALERTA
        alert(`❌ Solo tenemos ${maxStock} unidades disponibles`);
    }
}

function decreaseQuantity(itemId) {
    const input = document.getElementById(`quantity-input-${itemId}`);
    let value = parseInt(input.value) || 1;

    if (value > 1) {
        value--;
        input.value = value;
        // ENVIAR AL SERVIDOR
        actualizarCantidad(itemId, value);
    }
}

// Horario programado //
const tipoEntregaSelect = document.getElementById('tipo-entrega');

if (tipoEntregaSelect) {
    tipoEntregaSelect.addEventListener('change', function() {
        const programadaFields = document.getElementById('programada-fields');
        
        if (this.value === 'programada') {
            programadaFields.style.display = 'block';

            const pasadoMañana = new Date();
            pasadoMañana.setDate(pasadoMañana.getDate() + 2);
            const fechaMinima = pasadoMañana.toISOString().split('T')[0];

            document.getElementById('fecha-programada').min = fechaMinima;
            document.getElementById('fecha-programada').value = fechaMinima;

        } else {
            programadaFields.style.display = 'none';
        }
    });
}




// Lógica de mostrar/ocultar botón "Confirmar Pedido" según método de pago //
(function() {
  document.addEventListener('DOMContentLoaded', function() {

    const confirmarBtns = document.querySelectorAll('#confirmar-pedido-btn');
    if (confirmarBtns.length === 0) {
      return;
    }

    // --- Helpers de logging ---
    function log(...args){ console.log('[PagoUI]', ...args); }
    function warn(...args){ console.warn('[PagoUI]', ...args); }
    function error(...args){ console.error('[PagoUI]', ...args); }

    // --- Buscar elementos ---
    const radios = document.querySelectorAll('input[name="metodo_pago"]');
    const seccionNequi = document.getElementById('seccion-nequi');
    const seccionDaviplata = document.getElementById('seccion-daviplata');

    log('Sección Nequi encontrada:', !!seccionNequi);
    log('Sección DaviPlata encontrada:', !!seccionDaviplata);

    log('Botones encontrados con id #confirmar-pedido-btn:', confirmarBtns.length);
    if (confirmarBtns.length === 0) {
      error('No se encontró ningún elemento con id "confirmar-pedido-btn". Revisa que el id exista exactamente.');
      return;
    }
    if (confirmarBtns.length > 1) {
      warn('Hay más de un elemento con id "confirmar-pedido-btn". Debes tener solo uno. Esto puede romper la lógica.');
    }

    // Tomamos el primer botón como origen de verdad
    const confirmarBtn = confirmarBtns[0];

    // --- Forzar ocultamiento por CSS (fallback muy fuerte) ---
    // Añadimos una regla CSS !important para asegurarnos que esté oculto hasta que lo mostremos nosotros.
    const styleId = 'pagoui-force-style';
    if (!document.getElementById(styleId)) {
      const style = document.createElement('style');
      style.id = styleId;
      style.innerHTML = `
        #confirmar-pedido-btn { display: none !important; opacity: 1 !important; visibility: visible !important; }
      `;
      document.head.appendChild(style);
      log('Regla CSS insertada para forzar ocultamiento inicial.');
    }

    // Asegurarnos de que el botón empiece oculto (doble seguridad)
    confirmarBtn.style.setProperty('display', 'none', 'important');
    confirmarBtn.disabled = true;

    // --- Función para mostrar/ocultar botón ---
    function mostrarBoton(show) {
      if (show) {
        confirmarBtn.style.setProperty('display', 'block', 'important');
        confirmarBtn.disabled = false;
        log('Botón mostrado (efectivo seleccionado).');
      } else {
        confirmarBtn.style.setProperty('display', 'none', 'important');
        confirmarBtn.disabled = true;
        log('Botón oculto (no efectivo).');
      }
    }

    // Inicial: oculto
    mostrarBoton(false);

    // --- Registrar listeners en radios ---
    if (radios.length === 0) {
      warn('No se encontraron radios de metodo_pago. Verifica el name="metodo_pago" en los inputs.');
    }
    radios.forEach(radio => {
        radio.addEventListener('change', function() {
            log('Cambio de método detectado:', this.value, 'checked:', this.checked);
            if (this.checked && this.value === 'efectivo') {
                mostrarBoton(true);
                // OCULTAR secciones de pago digital
                if(seccionNequi) seccionNequi.style.display = 'none';
                if(seccionDaviplata) seccionDaviplata.style.display = 'none';
            } else if (this.checked && this.value === 'nequi') {
                mostrarBoton(false);
                // MOSTRAR Nequi, OCULTAR DaviPlata
                if(seccionNequi) seccionNequi.style.display = 'block';
                if(seccionDaviplata) seccionDaviplata.style.display = 'none';
            } else if (this.checked && this.value === 'daviplata') {
                mostrarBoton(false);
                // MOSTRAR DaviPlata, OCULTAR Nequi
                if(seccionNequi) seccionNequi.style.display = 'none';
                if(seccionDaviplata) seccionDaviplata.style.display = 'block';
            }
        });
    });

    // --- Diagnostic: imprimir estado actual en consola (útil para probar) ---
    log('Estado inicial de radios:');
    radios.forEach(r => log('  ', r.value, 'checked=', r.checked));

    // --- Observador: detectar si otro script cambia el estilo del botón ---
    const observer = new MutationObserver(function(mutationsList) {
      for (const m of mutationsList) {
        if (m.type === 'attributes' && (m.attributeName === 'style' || m.attributeName === 'class')) {
          const computed = window.getComputedStyle(confirmarBtn);
          // Si está visible y no debería, avisamos
          if (computed.display !== 'none' && confirmarBtn.disabled === true) {
            warn('El botón aparece visible pero está marcado como disabled = true — algo externo lo mostró. Volviendo a ocultar.');
            mostrarBoton(false);
          }
        }
      }
    });
    observer.observe(confirmarBtn, { attributes: true, attributeFilter: ['style','class'] });

    // --- Comando rápido para depuración desde consola ---
    window.__pagoUI = {
      mostrarBoton,
      confirmarBtn,
      radios,
      forceHide: () => { mostrarBoton(false); log('forceHide ejecutado'); },
      forceShow: () => { mostrarBoton(true); log('forceShow ejecutado'); },
    };

    log('PagoUI listo. Usa window.__pagoUI.forceShow() / forceHide() en la consola para probar.');

  }); // DOMContentLoaded
})();


// Filtro de domiciliario //
document.addEventListener('DOMContentLoaded', function() {
    const filtro = document.getElementById('filtro-domiciliario');
    
    // ✅ VERIFICACIÓN CRÍTICA: Solo ejecutar si existe el filtro
    if (!filtro) {
        return; // Salir silenciosamente si no estamos en el dashboard domiciliario
    }
    
    console.log("✅ Filtro de domiciliario inicializado");
    
    filtro.addEventListener('change', function() {
        const selectedDomi = this.value;
        const rows = document.querySelectorAll('table tr');
        
        // Empezar desde 1 para saltar el header (fila 0)
        for (let i = 1; i < rows.length; i++) {
            const cells = rows[i].querySelectorAll('td');
            
            // ✅ VERIFICAR que la fila tiene suficientes celdas (la 13 es domiciliario)
            if (cells.length >= 13) {
                const domiCell = cells[12]; // Celda 13 (índice 12) es domiciliario
                const domiName = domiCell.textContent.trim();
                
                // Mostrar/ocultar según el filtro
                if (selectedDomi === "" || domiName === selectedDomi) {
                    rows[i].style.display = ''; // Mostrar
                } else {
                    rows[i].style.display = 'none'; // Ocultar
                }
            }
        }
    });
});



// AUTO-REFRESH PARA SEGUIMIENTO Y DASHBOARDS

document.addEventListener('DOMContentLoaded', function() {
    const urlPath = window.location.pathname;
    
    // 1. VERIFICAR SI ESTAMOS EN SEGUIMIENTO
    if (urlPath.includes('/seguimiento/')) {
        console.log('📍 Detectada página de seguimiento, activando auto-refresh...');
        activarAutoRefreshSeguimiento();
    }
    
    // 2. VERIFICAR SI ESTAMOS EN DASHBOARD
    if (urlPath.includes('dashboard')) {
        console.log('📊 Detectado dashboard, activando auto-refresh...');
        activarAutoRefreshDashboard();
    }
});

function activarAutoRefreshSeguimiento() {
    // Solo activar si encontramos texto de "seguimiento"
    const elementos = document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, div');
    let encontrado = false;
    
    elementos.forEach(el => {
        if (el.textContent.toLowerCase().includes('seguimiento')) {
            encontrado = true;
        }
    });
    
    if (!encontrado) return;
    
    console.log('✅ Auto-refresh activado para seguimiento (30s)');
    
    let segundos = 30;
    const contador = document.createElement('div');
    contador.id = 'refresh-contador';
    contador.style.cssText = 'text-align: center; font-size: 0.9rem; color: #888; margin: 15px 0; padding: 5px; background: #2a2a2a; border-radius: 5px;';
    contador.innerHTML = `🔄 Actualizando en <strong style="color: var(--primary-color);">${segundos}</strong> segundos`;
    
    // Insertar en la página
    const container = document.querySelector('.schedule-box-2, .container, body');
    if (container) {
        container.prepend(contador);
    }
    
    const intervalo = setInterval(function() {
        segundos--;
        contador.innerHTML = `🔄 Actualizando en <strong style="color: var(--primary-color);">${segundos}</strong> segundos`;
        
        if (segundos <= 0) {
            clearInterval(intervalo);
            contador.innerHTML = '🔄 Actualizando...';
            setTimeout(() => location.reload(), 500);
        }
    }, 1000);
}

function activarAutoRefreshDashboard() {
    console.log('✅ Auto-refresh activado para dashboard (60s)');
    
    // Agregar indicador visual pequeño
    const indicador = document.createElement('div');
    indicador.id = 'dashboard-refresh-indicator';
    indicador.style.cssText = 'position: fixed; bottom: 10px; right: 10px; background: #2a2a2a; color: #888; padding: 5px 10px; border-radius: 5px; font-size: 0.8rem; z-index: 1000;';
    indicador.innerHTML = '🔄 Dashboard auto-refresh activado';
    document.body.appendChild(indicador);
    
    // Contador de tiempo
    let segundos = 60;
    const actualizarIndicador = () => {
        segundos--;
        indicador.innerHTML = `🔄 Recargando en ${segundos}s`;
        if (segundos <= 0) segundos = 60;
    };
    
    // Actualizar cada segundo
    setInterval(actualizarIndicador, 1000);
    
    // Recargar cada 60 segundos
    setInterval(function() {
        indicador.innerHTML = '🔄 Recargando ahora...';
        setTimeout(() => location.reload(), 500);
    }, 60000);
}

// Cerrar menú móvil al hacer click en un enlace //
document.addEventListener('DOMContentLoaded', function() {
    // Cerrar menú móvil al hacer click en cualquier enlace del navbar
    document.querySelectorAll('.navbar-nav .nav-link').forEach(function(link) {
        link.addEventListener('click', function() {
            // Solo en móvil (ancho < 768px)
            if (window.innerWidth < 768) {
                var navbar = document.getElementById('navbarSupportedContent');
                if (navbar && navbar.classList.contains('show')) {
                    // Bootstrap 5: cerrar el menú
                    var bsCollapse = new bootstrap.Collapse(navbar);
                    bsCollapse.hide();
                }
            }
        });
    });
});
