document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const nombreArchivo = params.get('archivo');

    if (nombreArchivo) {
        fetch(`http://127.0.0.1:5000/reporte_por_archivo?archivo=${nombreArchivo}`)
            .then(response => response.json())
            .then(data => mostrarDatosEnReporte(data))
            .catch(err => console.error("Error al cargar el reporte:", err));
    } else {
        alert("No se especificó el archivo del reporte");
    }
});

function mostrarDatosEnReporte(data) {
    document.getElementById('psicologo-nombre').textContent = `${data.psicologo.nombre} ${data.psicologo.apellido}`;
    document.getElementById('paciente-nombre').textContent = `${data.paciente.Nombre} ${data.paciente.Apellidos}`;
    document.getElementById('fecha-inicio').textContent = new Date(data.timestamp_inicio).toLocaleString();
    document.getElementById('fecha-fin').textContent = new Date(data.timestamp_fin).toLocaleString();

    // Emociones
    const emocionesUl = document.getElementById('lista-emociones');
    data.emociones.forEach(e => {
        const li = document.createElement('li');
        li.textContent = `Emoción: ${e.emocion}, Score: ${e.score}, Tiempo: ${e.timestamp}`;
        emocionesUl.appendChild(li);
    });

    // Alertas
    const alertasUl = document.getElementById('lista-alertas');
    data.alertas.forEach(a => {
        const li = document.createElement('li');
        li.textContent = `[${a.tipo}] ${a.detalle || ''} (${a.emocion} - ${a.timestamp})`;
        alertasUl.appendChild(li);
    });

    // Transcripciones
    const transUl = document.getElementById('lista-transcripciones');
    data.voz.forEach(v => {
        const li = document.createElement('li');
        li.textContent = `Texto: ${v.texto} | Emoción: ${v.emocion} | Hora: ${v.timestamp}`;
        transUl.appendChild(li);
    });

    // Posturas
    const posturasUl = document.getElementById('lista-posturas');
    data.posturas.forEach(p => {
        const li = document.createElement('li');
        li.textContent = `Postura: ${p.postura} - Tiempo: ${p.timestamp}`;
        posturasUl.appendChild(li);
    });

    // Capturas
    const galeria = document.getElementById('galeria-capturas');
    data.capturas.forEach(c => {
        const div = document.createElement('div');
        div.innerHTML = `
            <p><strong>${c.descripcion}</strong> (${c.timestamp})</p>
            <img src="../../${c.ruta}" alt="Captura crítica" style="max-width: 300px; border: 1px solid #ccc; margin-bottom: 10px;">
        `;
        galeria.appendChild(div);
    });
}
