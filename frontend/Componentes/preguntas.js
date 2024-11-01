// Función para obtener todas las preguntas
function obtenerPreguntas() {
    fetch('http://127.0.0.1:5000/obtener_preguntas')
        .then(response => response.json())
        .then(data => {
            const listaPreguntas = document.getElementById('listaPreguntas');
            listaPreguntas.innerHTML = '';
            
            data.preguntas.forEach((pregunta, index) => {
                const preguntaDiv = document.createElement('div');
                preguntaDiv.classList.add('question-item', 'd-flex', 'justify-content-between', 'align-items-center');
                
                preguntaDiv.innerHTML = `
                    <span>${index + 1}. ${pregunta.pregunta}</span>
                    <button class="btn btn-danger btn-sm" onclick="eliminarPregunta('${pregunta._id}')">Eliminar</button>
                `;
                listaPreguntas.appendChild(preguntaDiv);
            });
        })
        .catch(error => console.error('Error al obtener las preguntas:', error));
}

// Función para agregar una nueva pregunta
document.getElementById('agregarPreguntaBtn').addEventListener('click', () => {
    const nuevaPregunta = document.getElementById('nuevaPregunta').value.trim();
    if (nuevaPregunta) {
        fetch('http://127.0.0.1:5000/agregar_pregunta', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pregunta: nuevaPregunta })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            obtenerPreguntas(); // Recargar la lista de preguntas
            document.getElementById('nuevaPregunta').value = ''; // Limpiar el campo de entrada
        })
        .catch(error => console.error('Error al agregar la pregunta:', error));
    } else {
        alert("Por favor, ingresa una pregunta.");
    }
});

// Función para eliminar una pregunta
function eliminarPregunta(id) {
    fetch('http://127.0.0.1:5000/eliminar_pregunta', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        obtenerPreguntas(); // Recargar la lista de preguntas
    })
    .catch(error => console.error('Error al eliminar la pregunta:', error));
}

// Cargar las preguntas al cargar la página
document.addEventListener('DOMContentLoaded', obtenerPreguntas);
