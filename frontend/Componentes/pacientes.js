// Lista de estudiantes (usada localmente para el estado temporal)
let estudiantes = [];

// Mostrar mensajes de error
function mostrarError(mensaje, campoId = null) {
  let errorDiv = document.getElementById('errorMensaje');
  if (!errorDiv) {
    errorDiv = document.createElement('div');
    errorDiv.id = 'errorMensaje';
    errorDiv.className = 'alert alert-danger mt-2';
    document.getElementById('formPaciente').prepend(errorDiv);
  }
  errorDiv.textContent = mensaje;

  if (campoId) {
    const campo = document.getElementById(campoId);
    campo.classList.add('is-invalid');
  }
}

function mostrarFeedback(campoId, mensaje) {
  let feedback = document.getElementById(`${campoId}-feedback`);
  if (!feedback) {
    feedback = document.createElement('div');
    feedback.id = `${campoId}-feedback`;
    feedback.className = 'invalid-feedback';
    document.getElementById(campoId).after(feedback);
  }
  feedback.textContent = mensaje;
}

function limpiarErrores() {
  const errorDiv = document.getElementById('errorMensaje');
  if (errorDiv) errorDiv.remove();

  const campos = ['nombre', 'apellidos', 'edad', 'genero', 'telefono'];
  campos.forEach(id => {
    document.getElementById(id).classList.remove('is-invalid');
    const fb = document.getElementById(`${id}-feedback`);
    if (fb) fb.remove();
  });
}

function validarCampoIndividual(campoId) {
  const valor = document.getElementById(campoId).value;
  const soloLetras = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$/;
  const soloNumeros = /^\d+$/;
  let valido = true;
  let mensaje = '';

  switch (campoId) {
    case 'nombre':
      valido = soloLetras.test(valor) && valor.trim().length >= 2;
      mensaje = 'Solo letras, mínimo 2 caracteres';
      break;
    case 'apellidos':
      valido = soloLetras.test(valor) && valor.trim().length >= 2;
      mensaje = 'Solo letras, mínimo 2 caracteres';
      break;
    case 'edad':
      const edad = parseInt(valor);
      valido = !isNaN(edad) && edad >= 5 && edad <= 100;
      mensaje = 'Número entre 5 y 100';
      break;
    case 'genero':
      const genero = valor.toLowerCase();
      valido = genero === 'masculino' || genero === 'femenino';
      mensaje = 'Solo "Masculino" o "Femenino"';
      break;
    case 'telefono':
      valido = soloNumeros.test(valor) && valor.length >= 7 && valor.length <= 10;
      mensaje = 'Solo números, 7 a 10 dígitos';
      break;
  }

  const campo = document.getElementById(campoId);
  if (!valido) {
    campo.classList.add('is-invalid');
    mostrarFeedback(campoId, mensaje);
  } else {
    campo.classList.remove('is-invalid');
    const fb = document.getElementById(`${campoId}-feedback`);
    if (fb) fb.remove();
  }
}

function validarCampos(paciente) {
  const soloLetras = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$/;
  const soloNumeros = /^\d+$/;

  if (!soloLetras.test(paciente.Nombre) || paciente.Nombre.trim().length < 2) {
    mostrarError("El nombre debe contener solo letras y al menos 2 caracteres.", 'nombre');
    return false;
  }

  if (!soloLetras.test(paciente.Apellidos) || paciente.Apellidos.trim().length < 2) {
    mostrarError("Los apellidos deben contener solo letras y al menos 2 caracteres.", 'apellidos');
    return false;
  }

  const edad = parseInt(paciente.Edad);
  if (isNaN(edad) || edad < 5 || edad > 100) {
    mostrarError("La edad debe ser un número entre 5 y 100.", 'edad');
    return false;
  }

  const genero = paciente.Genero.toLowerCase();
  if (genero !== "masculino" && genero !== "femenino") {
    mostrarError("El género debe ser 'Masculino' o 'Femenino'.", 'genero');
    return false;
  }

  if (!soloNumeros.test(paciente.Telefono) || paciente.Telefono.length < 7 || paciente.Telefono.length > 10) {
    mostrarError("El teléfono debe contener solo números (7 a 10 dígitos).", 'telefono');
    return false;
  }

  return true;
}

['nombre', 'apellidos', 'edad', 'genero', 'telefono'].forEach(id => {
  document.getElementById(id).addEventListener('input', () => validarCampoIndividual(id));
});

function obtenerEstudiantes() {
  fetch("http://127.0.0.1:5000/pacientes")
    .then(response => response.json())
    .then(data => {
      estudiantes = data;
      renderizarEstudiantes(data);
    })
    .catch(error => console.error('Error al obtener estudiantes:', error));
}

function renderizarEstudiantes(estudiantes) {
  const tablaPacientes = document.getElementById('tablaPacientes');
  tablaPacientes.innerHTML = '';

  estudiantes.forEach((paciente, index) => {
    const fila = document.createElement('tr');
    fila.innerHTML = `
      <td>${paciente.id_paciente || 'N/A'}</td>
      <td>${paciente.Nombre || 'N/A'}</td>
      <td>${paciente.Apellidos || 'N/A'}</td>
      <td>${paciente.Edad || 'N/A'}</td>
      <td>${paciente.Genero || 'N/A'}</td>
      <td>${paciente.Telefono || 'N/A'}</td>
      <td>
        <button class="btn btn-warning" onclick="editarEstudiante(${index})">Editar</button>
        <button class="btn btn-danger" onclick="eliminarEstudiante(${index})">Eliminar</button>
      </td>
    `;
    tablaPacientes.appendChild(fila);
  });
}

obtenerEstudiantes();

document.getElementById('formPaciente').addEventListener('submit', function(event) {
  event.preventDefault();

  const editIndex = document.getElementById('formPaciente').dataset.editIndex;

  const paciente = {
    Nombre: document.getElementById('nombre').value,
    Apellidos: document.getElementById('apellidos').value,
    Edad: document.getElementById('edad').value,
    Genero: document.getElementById('genero').value,
    Telefono: document.getElementById('telefono').value,
  };

  limpiarErrores();
  if (!validarCampos(paciente)) return;

  if (editIndex !== undefined) {
    paciente.id_paciente = document.getElementById('id_paciente').value;
    fetch(`http://127.0.0.1:5000/pacientes/${paciente.id_paciente}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(paciente),
    })
      .then(() => {
        obtenerEstudiantes();
        document.getElementById('formPaciente').reset();
        delete document.getElementById('formPaciente').dataset.editIndex;
        document.getElementById('id_paciente').disabled = true;
      })
      .catch(error => console.error('Error al actualizar estudiante:', error));
  } else {
    fetch('http://127.0.0.1:5000/pacientes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(paciente),
    })
      .then(() => {
        obtenerEstudiantes();
        document.getElementById('formPaciente').reset();
        document.getElementById('id_paciente').value = '';
      })
      .catch(error => console.error('Error al agregar estudiante:', error));
  }
});

function editarEstudiante(index) {
  const paciente = estudiantes[index];
  document.getElementById('id_paciente').value = paciente.id_paciente;
  document.getElementById('nombre').value = paciente.Nombre;
  document.getElementById('apellidos').value = paciente.Apellidos;
  document.getElementById('edad').value = paciente.Edad;
  document.getElementById('genero').value = paciente.Genero;
  document.getElementById('telefono').value = paciente.Telefono;

  document.getElementById('formPaciente').dataset.editIndex = index;
  document.getElementById('id_paciente').disabled = true;
}

function eliminarEstudiante(index) {
  const id_paciente = estudiantes[index].id_paciente;
  const nombre = estudiantes[index].Nombre;
  const confirmado = confirm(`¿Estás seguro de que deseas eliminar al paciente ${nombre}? Esta acción no se puede deshacer.`);
  if (!confirmado) return;
  fetch(`http://127.0.0.1:5000/pacientes/${id_paciente}`, {
    
    method: 'DELETE',
  })
    .then(() => obtenerEstudiantes())
    .catch(error => console.error('Error al eliminar estudiante:', error));
}
