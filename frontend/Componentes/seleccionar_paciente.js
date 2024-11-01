document.addEventListener("DOMContentLoaded", function() {
    const pacienteSelect = document.getElementById("paciente");
  
    // Obtener lista de pacientes del backend y mostrarla en el menú desplegable
    fetch("http://127.0.0.1:5000/pacientes")
      .then(response => response.json())
      .then(data => {
        data.forEach(paciente => {
          const option = document.createElement("option");
          option.value = paciente.id_paciente; // Suponiendo que cada paciente tiene un id_paciente único
          option.textContent = `${paciente.Nombre} ${paciente.Apellidos}`;
          pacienteSelect.appendChild(option);
        });
      })
      .catch(error => console.error("Error al obtener pacientes:", error));
  
    // Manejar el evento de envío del formulario
    document.getElementById("seleccionarPacienteForm").addEventListener("submit", function(event) {
      event.preventDefault();
      
      const pacienteId = pacienteSelect.value;
      if (pacienteId) {
        // Redirigir a la página de diagnóstico con el paciente seleccionado
        window.location.href = `diagnostico_vivo.html?pacienteId=${pacienteId}`;
      } else {
        alert("Por favor, seleccione un paciente.");
      }
    });
  });
  