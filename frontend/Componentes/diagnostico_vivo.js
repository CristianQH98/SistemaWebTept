// Función para cargar los datos del psicólogo y del paciente
function cargarDatos() {
    const usuarioActual = JSON.parse(localStorage.getItem('usuarioActual'));
    if (usuarioActual) {
        document.getElementById('datosPsicologo').innerHTML = `
            Nombre del Psicólogo: ${usuarioActual.nombre} ${usuarioActual.apellido}
        `;
    } else {
        document.getElementById('datosPsicologo').innerHTML = 'Información del psicólogo no disponible';
    }

    const urlParams = new URLSearchParams(window.location.search);
    const pacienteId = urlParams.get('pacienteId');

    fetch(`http://127.0.0.1:5000/pacientes/${pacienteId}`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                document.getElementById('datosPaciente').innerHTML = `
                    Nombre del Paciente: ${data.Nombre} ${data.Apellidos}, ${data.Edad} años
                `;
            } else {
                document.getElementById('datosPaciente').innerHTML = 'Información del paciente no disponible';
            }
        })
        .catch(error => console.error('Error al obtener los datos del paciente:', error));
}

function actualizarFechaHora() {
    const fechaHoraElemento = document.getElementById('fechaHoraActual');
    if (fechaHoraElemento) {
        const ahora = new Date();
        const opciones = { 
            day: '2-digit', month: '2-digit', year: 'numeric',
            hour: '2-digit', minute: '2-digit', second: '2-digit' 
        };
        fechaHoraElemento.textContent = ahora.toLocaleDateString('es-ES', opciones);
    }
}

// Inicia la actualización de fecha y hora al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    cargarDatos();
    actualizarFechaHora();
    setInterval(actualizarFechaHora, 1000); // Actualiza cada segundo
});

// Función para iniciar el flujo de video
function iniciarFlujo() {
    const videoContainer = document.getElementById('videoStream');
    videoContainer.src = 'http://127.0.0.1:5000/video_feed';
    videoContainer.onerror = reconectarFlujo;
}

// Función para reconectar el flujo de video
function reconectarFlujo() {
    console.log("Conexión de video perdida. Intentando reconectar...");
    setTimeout(iniciarFlujo, 2000); // Intenta reconectar después de 2 segundos
}

//funcion para capturar audio
function iniciarGrabacion(preguntaId) {
    // Llamada al backend para iniciar la captura de audio y análisis
    fetch('http://127.0.0.1:5000/capturar_audio')
      .then(response => response.json())
      .then(data => {
        const textoTranscrito = data.texto_transcrito;
        const emocionDetectada = data.emocion;
        
        // Actualiza el cuadro de texto de la pregunta correspondiente
        const respuestaTextarea = document.getElementById(`respuesta${preguntaId}`);
        respuestaTextarea.value = `Texto: ${textoTranscrito}\nEmoción: ${emocionDetectada}`;
      })
      .catch(error => console.error('Error en la captura de audio:', error));
  }
  function cargarPreguntas() {
    fetch('http://127.0.0.1:5000/obtener_preguntas')
        .then(response => response.json())
        .then(data => {
            const preguntasContainer = document.getElementById('preguntasContainer');
            preguntasContainer.innerHTML = ''; // Limpiar contenido anterior

            data.preguntas.forEach((item, index) => {
                const preguntaDiv = document.createElement('div');
                preguntaDiv.classList.add('pregunta-item', 'mb-3');
                
                preguntaDiv.innerHTML = `
                    <p><strong>Pregunta ${index + 1}:</strong> ${item.pregunta}</p>
                    <div class="form-group">
                        <textarea id="respuesta-${index}" class="form-control" placeholder="Respuesta"></textarea>
                        <button onclick="grabarRespuesta(${index})" class="btn btn-primary mt-2">Grabar Respuesta</button>
                    </div>
                `;
                
                preguntasContainer.appendChild(preguntaDiv);
            });
        })
        .catch(error => console.error('Error al cargar las preguntas:', error));
}

function grabarRespuesta(index) {
    fetch('http://127.0.0.1:5000/grabar_respuesta')
        .then(response => response.json())
        .then(data => {
            const respuestaTextarea = document.getElementById(`respuesta-${index}`);
            const emocion = data.emociones_especificas.join(', ') || "Desconocido"; // Maneja el caso de que no haya emociones
            respuestaTextarea.value = `Texto: ${data.texto} | Sentimiento: ${data.sentimiento_general} | Emociones: ${emocion}`;
        })
        .catch(error => console.error('Error al grabar la respuesta:', error));
}


document.addEventListener('DOMContentLoaded', () => {
    cargarPreguntas();
});
// Iniciar el flujo de video al cargar la página
document.addEventListener('DOMContentLoaded', iniciarFlujo);
