// Función para cargar los datos del psicólogo y del estudiante
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
    const pacienteId = urlParams.get('id_paciente');
    console.log("Estudiante ID recibido:", pacienteId); // Para depurar

    if (pacienteId) {
        fetch(`http://127.0.0.1:5000/pacientes/${pacienteId}`)
            .then(response => response.json())
            .then(data => {
                if (data && data.Nombre && data.Apellidos) {
                    document.getElementById('datosPaciente').innerHTML = `
                        Nombre del Estudiante: ${data.Nombre} ${data.Apellidos}, ${data.Edad} años
                    `;
                } else {
                    document.getElementById('datosPaciente').innerHTML = 'Información del estudiante no disponible';
                }
            })
            .catch(error => {
                console.error('Error al obtener los datos del estudiante:', error);
                document.getElementById('datosPaciente').innerHTML = 'Error al cargar información del estudiante';
            });
    } else {
        document.getElementById('datosPaciente').innerHTML = 'ID del estudiante no proporcionado';
    }
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

document.addEventListener('DOMContentLoaded', () => {
    cargarDatos();
    actualizarFechaHora();
    setInterval(actualizarFechaHora, 1000);
});

function iniciarFlujo() {
    const videoContainer = document.getElementById('videoStream');
    videoContainer.src = 'http://127.0.0.1:5000/video_feed';
    videoContainer.onerror = reconectarFlujo;
}

function reconectarFlujo() {
    console.log("Conexión de video perdida. Intentando reconectar...");
    setTimeout(iniciarFlujo, 2000);
}

function iniciarGrabacion(preguntaId) {
    fetch('http://127.0.0.1:5000/capturar_audio')
      .then(response => response.json())
      .then(data => {
        const textoTranscrito = data.texto_transcrito;
        const emocionDetectada = data.emocion;
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
            preguntasContainer.innerHTML = '';

            if (data.preguntas && data.preguntas.length > 0) {
                data.preguntas.forEach((item, index) => {
                    const preguntaDiv = document.createElement('div');
                    preguntaDiv.classList.add('pregunta-item', 'mb-3');
                    preguntaDiv.id = `pregunta-${index}`;

                    preguntaDiv.innerHTML = `
                        <p><strong>Pregunta ${index + 1}:</strong> ${item.pregunta}</p>
                        <div class="form-group">
                            <textarea id="respuesta-${index}" class="form-control" placeholder="Respuesta"></textarea>
                            <div class="mt-2">
                                <button onclick="grabarRespuesta(${index})" class="btn btn-primary mr-2">Grabar Respuesta</button>
                                <button onclick="siguientePregunta()" class="btn btn-secondary">Siguiente Pregunta</button>
                            </div>
                        </div>
                    `;

                    preguntasContainer.appendChild(preguntaDiv);
                    if (index > 0) {
                        preguntaDiv.style.display = 'none';
                    }
                });

                let preguntaActualIndex = 0;
                const preguntas = document.querySelectorAll('.pregunta-item');

                window.siguientePregunta = () => {
                    if (preguntaActualIndex < preguntas.length - 1) {
                        $(preguntas[preguntaActualIndex]).fadeOut(() => {
                            preguntaActualIndex++;
                            $(preguntas[preguntaActualIndex]).fadeIn();
                        });
                    } else {
                        alert('Has llegado a la última pregunta.');
                    }
                };
            } else {
                preguntasContainer.innerHTML = '<p>No hay preguntas disponibles.</p>';
            }
        })
        .catch(error => console.error('Error al cargar las preguntas:', error));
}

function finalizarSesion() {
    fetch('http://127.0.0.1:5000/probar_diagnostico')
        .then(response => response.json())
        .then(data => {
            console.log("Diagnóstico finalizado:", data);

            const nombreArchivo = data.archivo;

            // Guardar el reporte en MongoDB
            fetch('http://127.0.0.1:5000/guardar_reporte_bd', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ archivo: nombreArchivo })
            })
            .then(response => response.json())
            .then(dataMongo => {
                console.log("Reporte guardado en MongoDB:", dataMongo.mensaje);
                alert("Reporte guardado en la base de datos exitosamente");

                // Redirigir al HTML del reporte
                window.location.href = `reporte.html?archivo=${encodeURIComponent(nombreArchivo)}`;
            })
            .catch(error => {
                console.error("Error al guardar el reporte en MongoDB:", error);
                alert("No se pudo guardar el reporte en la base de datos");
            });

        })
        .catch(error => {
            console.error("Error durante el diagnóstico:", error);
            alert("Hubo un error al finalizar el diagnóstico");
        });
}



function grabarRespuesta(index) {
    fetch('http://127.0.0.1:5000/grabar_respuesta')
        .then(response => response.json())
        .then(data => {
            const respuestaTextarea = document.getElementById(`respuesta-${index}`);
            const emocion = data.emociones_especificas.join(', ') || "Desconocido";
            respuestaTextarea.value = `Texto: ${data.texto} | Sentimiento: ${data.sentimiento_general} | Emociones: ${emocion}`;
        })
        .catch(error => console.error('Error al grabar la respuesta:', error));
}

document.addEventListener('DOMContentLoaded', () => {
    cargarPreguntas();
});

document.addEventListener('DOMContentLoaded', iniciarFlujo);

// Esta función guarda el archivo .json en MongoDB
function guardarReporteEnMongoDB(nombreArchivo) {
    fetch('http://127.0.0.1:5000/guardar_reporte_bd', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ archivo: nombreArchivo })
    })
    .then(response => response.json())
    .then(data => {
        console.log(" Reporte guardado en MongoDB:", data.mensaje);
        alert(" Reporte guardado en la base de datos");
    })
    .catch(error => {
        console.error(" Error al guardar el reporte:", error);
        alert(" No se pudo guardar en la base de datos");
    });
}
