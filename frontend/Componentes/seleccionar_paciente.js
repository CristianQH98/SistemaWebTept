document.addEventListener("DOMContentLoaded", function () {
  const pacienteSelect = document.getElementById("paciente");

  // Obtener lista de pacientes del backend
  fetch("http://127.0.0.1:5000/pacientes")
    .then(response => response.json())
    .then(data => {
      data.forEach(paciente => {
        const option = document.createElement("option");
        option.value = paciente.id_paciente;
        option.textContent = `${paciente.Nombre} ${paciente.Apellidos}`;
        pacienteSelect.appendChild(option);
      });
    })
    .catch(error => console.error("Error al obtener pacientes:", error));

  // Al enviar el formulario, guardar el paciente seleccionado en localStorage
  document.getElementById("seleccionarPacienteForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const pacienteId = pacienteSelect.value;
    if (pacienteId) {
      fetch(`http://127.0.0.1:5000/pacientes/${pacienteId}`)
        .then(response => response.json())
        .then(paciente => {
          localStorage.setItem("pacienteSeleccionado", JSON.stringify(paciente));
          window.location.href = "../componentes/diagnostico_vivo.html";
        })
        .catch(error => {
          console.error("Error al obtener los datos del paciente:", error);
          alert("No se pudo cargar la información del estudiante.");
        });
    } else {
      alert("Por favor, seleccione un Estudiante.");
    }
  });
});
