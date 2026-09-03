// Estado de la aplicación
let selectedProduct = {
  name: "Llavero Metálico Turbo",
  price: 5000,
  chances: 3
};

// Configuración de API (Fallback local si corre con FastAPI)
const API_URL = window.location.origin.includes(':8000') || window.location.origin.includes('127.0.0.1') || window.location.origin.includes('localhost')
  ? '/api'
  : 'http://127.0.0.1:8000/api';

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
  initCountdown();
  initAngleControls();
});

// 1. Reloj de cuenta regresiva
function initCountdown() {
  const targetDate = new Date();
  targetDate.setDate(targetDate.getDate() + 14); // 14 días a partir de hoy

  function update() {
    const now = new Date().getTime();
    const diff = targetDate.getTime() - now;

    if (diff <= 0) return;

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);

    document.getElementById('days').innerText = String(days).padStart(2, '0');
    document.getElementById('hours').innerText = String(hours).padStart(2, '0');
    document.getElementById('minutes').innerText = String(minutes).padStart(2, '0');
    document.getElementById('seconds').innerText = String(seconds).padStart(2, '0');
  }

  update();
  setInterval(update, 1000);
}

// 2. Control de ángulos y animación interactiva del auto
function initAngleControls() {
  const angleBtns = document.querySelectorAll('.angle-btn');
  const carDisplay = document.getElementById('carDisplay');

  angleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      angleBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const target = btn.dataset.target;
      // Rotación y transformación interactiva según el ángulo seleccionado
      switch (target) {
        case 'frontal':
          carDisplay.style.transform = 'perspective(800px) rotateY(0deg) scale(1)';
          break;
        case 'lateral':
          carDisplay.style.transform = 'perspective(800px) rotateY(15deg) scale(1.02)';
          break;
        case 'interior':
          carDisplay.style.transform = 'perspective(800px) rotateX(10deg) scale(1.08)';
          break;
        case 'trasera':
          carDisplay.style.transform = 'perspective(800px) rotateY(-15deg) scale(0.98)';
          break;
      }
    });
  });
}

// 3. Modal de Compra y Checkout
function openCheckout(productName, price, chances) {
  selectedProduct = {
    name: productName,
    price: price,
    chances: chances
  };

  document.getElementById('modalProductName').innerText = productName;
  document.getElementById('modalProductPrice').innerText = `$${price.toLocaleString('es-AR')}`;
  document.getElementById('modalProductChances').innerText = `${chances} ${chances === 1 ? 'Chance' : 'Chances'}`;

  // Reset stages
  document.getElementById('checkoutFormStage').classList.remove('hidden');
  document.getElementById('checkoutSuccessStage').classList.add('hidden');

  document.getElementById('checkoutModal').classList.add('active');
}

function closeCheckout() {
  document.getElementById('checkoutModal').classList.remove('active');
}

// Cerrar haciendo clic en el fondo
document.getElementById('checkoutModal').addEventListener('click', (e) => {
  if (e.target.id === 'checkoutModal') {
    closeCheckout();
  }
});

// 4. Procesar Registro y Envío a la Planilla
async function handleParticipantSubmit(event) {
  event.preventDefault();

  const form = document.getElementById('participantForm');
  const btnSubmit = document.getElementById('btnSubmit');
  const btnText = document.getElementById('btnText');
  const btnSpinner = document.getElementById('btnSpinner');

  const nombre = document.getElementById('nombre').value.trim();
  const email = document.getElementById('email').value.trim();
  const telefono = document.getElementById('telefono').value.trim();
  const dni = document.getElementById('dni').value.trim();
  const medioPago = form.elements['payment_method'].value;

  // Feedback de carga
  btnSubmit.disabled = true;
  btnText.innerText = 'Registrando en Google Sheets...';
  btnSpinner.classList.remove('hidden');

  const payload = {
    nombre: nombre,
    email: email,
    telefono: telefono,
    dni: dni,
    producto: selectedProduct.name,
    monto: selectedProduct.price,
    chances: selectedProduct.chances,
    medio_pago: medioPago
  };

  try {
    const response = await fetch(`${API_URL}/participar`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (response.ok && data.success) {
      if (data.payment_url) {
        window.location.href = data.payment_url;
      } else {
        showSuccess(data);
      }
    } else {
      // Si falla o no está conectado el backend, usar modo simulación amigable
      console.warn("API offline o error, procesando en modo simulación local:", data);
      simulateSuccess(payload);
    }
  } catch (error) {
    console.warn("Backend no disponible por el momento, generando tickets locales:", error);
    simulateSuccess(payload);
  } finally {
    btnSubmit.disabled = false;
    btnText.innerText = 'Continuar y Registrar Pago';
    btnSpinner.classList.add('hidden');
  }
}

// 5. Pantalla de Éxito y Confetti
function showSuccess(data) {
  document.getElementById('checkoutFormStage').classList.add('hidden');
  document.getElementById('checkoutSuccessStage').classList.remove('hidden');

  document.getElementById('successName').innerText = data.nombre;
  document.getElementById('successDni').innerText = data.dni;
  document.getElementById('successProduct').innerText = `${data.producto} (${data.chances} chances)`;

  const container = document.getElementById('assignedTicketNumbers');
  container.innerHTML = '';
  data.tickets.forEach(ticket => {
    const span = document.createElement('span');
    span.className = 'ticket-badge';
    span.innerText = `#${ticket}`;
    container.appendChild(span);
  });

  // Disparar confetti de celebración
  if (typeof confetti === 'function') {
    confetti({
      particleCount: 120,
      spread: 70,
      origin: { y: 0.6 }
    });
  }

  // Incrementar contador simulado en la web
  const liveCounter = document.getElementById('liveTicketsSold');
  if (liveCounter) {
    liveCounter.innerText = parseInt(liveCounter.innerText) + data.chances;
  }
}

// Simulación local de respaldo si el backend aún no está iniciado
function simulateSuccess(payload) {
  const tickets = [];
  for (let i = 0; i < payload.chances; i++) {
    const num = Math.floor(10000 + Math.random() * 90000);
    tickets.push(`AUTO-${num}`);
  }

  showSuccess({
    success: true,
    nombre: payload.nombre,
    dni: payload.dni,
    producto: payload.producto,
    chances: payload.chances,
    tickets: tickets
  });
}
