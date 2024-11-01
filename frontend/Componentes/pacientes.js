// Lista de pacientes (usada localmente para el estado temporal)
let pacientes = [];

// Función para obtener pacientes del backend
function obtenerPacientes() {
  fetch("http://127.0.0.1:5000/pacientes")
    .then(response => response.json())
    .then(data => {
      pacientes = data; // Actualizar lista local
      renderizarPacientes(data);
    })
    .catch(error => console.error('Error al obtener pacientes:', error));
}

// Función para renderizar pacientes en la tabla
function renderizarPacientes(pacientes) {
  const tablaPacientes = document.getElementById('tablaPacientes');
  tablaPacientes.innerHTML = ''; // Limpiar la tabla antes de agregar datos

  pacientes.forEach((paciente, index) => {
    const fila = document.createElement('tr');
    fila.innerHTML = `
      <td>${paciente.id_paciente || 'N/A'}</td>
      <td>${paciente.Nombre || 'N/A'}</td>
      <td>${paciente.Apellidos || 'N/A'}</td>
      <td>${paciente.Edad || 'N/A'}</td>
      <td>${paciente.Genero || 'N/A'}</td>
      <td>${paciente.Telefono || 'N/A'}</td>
      <td>
        <button class="btn btn-warning" onclick="editarPaciente(${index})">Editar</button>
        <button class="btn btn-danger" onclick="eliminarPaciente(${index})">Eliminar</button>
      </td>
    `;
    tablaPacientes.appendChild(fila);
  });
}

// Llama a obtenerPacientes para cargar los datos al iniciar
obtenerPacientes();

// Función para agregar o actualizar un paciente
document.getElementById('formPaciente').addEventListener('submit', function(event) {
  event.preventDefault();

  const editIndex = document.getElementById('formPaciente').dataset.editIndex;

  const paciente = {
    id_paciente: document.getElementById('id_paciente').value,
    Nombre: document.getElementById('nombre').value,
    Apellidos: document.getElementById('apellidos').value,
    Edad: document.getElementById('edad').value,
    Genero: document.getElementById('genero').value,
    Telefono: document.getElementById('telefono').value,
  };

  if (editIndex !== undefined) {
    // Actualizar paciente existente en el backend
    fetch(`http://127.0.0.1:5000/pacientes/${paciente.id_paciente}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(paciente),
    })
      .then(() => {
        obtenerPacientes();
        $('#modalPaciente').modal('hide');
        delete document.getElementById('formPaciente').dataset.editIndex;
      })
      .catch(error => console.error('Error al actualizar paciente:', error));
  } else {
    // Agregar nuevo paciente al backend
    fetch('http://127.0.0.1:5000/pacientes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(paciente),
    })
      .then(() => {
        obtenerPacientes();
        $('#modalPaciente').modal('hide');
      })
      .catch(error => console.error('Error al agregar paciente:', error));
  }
});

// Función para abrir el formulario de edición con datos prellenados
function editarPaciente(index) {
  const paciente = pacientes[index];
  document.getElementById('id_paciente').value = paciente.id_paciente;
  document.getElementById('nombre').value = paciente.Nombre;
  document.getElementById('apellidos').value = paciente.Apellidos;
  document.getElementById('edad').value = paciente.Edad;
  document.getElementById('genero').value = paciente.Genero;
  document.getElementById('telefono').value = paciente.Telefono;

  // Guardar el índice del paciente que se está editando
  document.getElementById('formPaciente').dataset.editIndex = index;

  $('#modalPaciente').modal('show');
}

// Función para eliminar un paciente
function eliminarPaciente(index) {
  const id_paciente = pacientes[index].id_paciente;

  fetch(`http://127.0.0.1:5000/pacientes/${id_paciente}`, {
    method: 'DELETE',
  })
    .then(() => obtenerPacientes())
    .catch(error => console.error('Error al eliminar paciente:', error));
}
