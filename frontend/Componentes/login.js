// Función para manejar el inicio de sesión y guardar los datos del psicólogo en localStorage
function autenticarUsuario(usuario, contraseña) {
    // Realizar la solicitud de autenticación al backend
    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ usuario, contraseña })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Autenticación exitosa: obtener datos completos del usuario
            fetch(`http://127.0.0.1:5000/usuarios/${usuario}`)
                .then(response => response.json())
                .then(userData => {
                    // Guardar los datos completos en localStorage
                    localStorage.setItem('usuarioActual', JSON.stringify(userData));
                    // Redirigir a la página correspondiente según el rol
                    if (userData.rol === 'psicologo') {
                        window.location.href = 'home.html';
                    } else if (userData.rol === 'administrador') {
                        window.location.href = 'administrador.html';
                    }
                })
                .catch(error => console.error('Error al obtener los datos del usuario:', error));
        } else {
            alert(data.message || 'Usuario o contraseña incorrectos');
        }
    })
    .catch(error => {
        console.error('Error en la autenticación:', error);
        alert('Error en el servidor');
    });
}

// Asociar la función al evento de envío del formulario de inicio de sesión
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const usuario = document.getElementById('usuario').value;
    const contraseña = document.getElementById('password').value;
    autenticarUsuario(usuario, contraseña);
});

// Función para cargar los datos del psicólogo y del paciente en `diagnostico_vivo.js`
function cargarDatos() {
    // Obtener datos del psicólogo desde localStorage
    const usuarioActual = JSON.parse(localStorage.getItem('usuarioActual'));
    console.log('Datos del psicólogo:', usuarioActual); // Verifica qué datos están en localStorage

    if (usuarioActual) {
      document.getElementById('datosPsicologo').innerHTML = `
        Nombre del Psicólogo: ${usuarioActual.nombre} ${usuarioActual.apellido}
      `;
    } else {
      console.log('Información del psicólogo no disponible en localStorage');
      document.getElementById('datosPsicologo').innerHTML = 'Información del psicólogo no disponible';
    }
  
    // Obtener el ID del paciente de la URL
    const urlParams = new URLSearchParams(window.location.search);
    const pacienteId = urlParams.get('pacienteId');
  
    // Obtener los datos del paciente desde el backend usando fetch
    fetch(`http://127.0.0.1:5000/pacientes/${pacienteId}`)
      .then(response => response.json())
      .then(data => {
        console.log('Datos del paciente:', data); // Verifica qué datos se reciben del backend
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

// Inicializar los datos en la carga de la página para `diagnostico_vivo.js`
document.addEventListener('DOMContentLoaded', cargarDatos);
