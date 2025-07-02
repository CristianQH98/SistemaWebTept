document.addEventListener("DOMContentLoaded", () => {
  const usuarioActual = JSON.parse(localStorage.getItem("usuarioActual"));

  if (usuarioActual) {
    document.getElementById("perfil-info").innerHTML = `
      <p><strong>Nombre:</strong> ${usuarioActual.nombre} ${usuarioActual.apellido}</p>
      <p><strong>Usuario:</strong> ${usuarioActual.usuario}</p>
      <p><strong>Rol:</strong> ${usuarioActual.rol}</p>
      <p><strong>Contraseña:</strong> ********</p>
      <button class="btn btn-secondary mt-2" data-bs-toggle="modal" data-bs-target="#modalCambiarContrasena">
        Cambiar Contraseña
      </button>
    `;
  } else {
    alert("No se encontró información del usuario logueado.");
  }

  document.getElementById("gestionar-preguntas").addEventListener("click", () => {
    window.location.href = "preguntas.html";
  });

  document.getElementById("guardarContrasena").addEventListener("click", () => {
    const nuevaContrasena = document.getElementById("nuevaContrasena").value;

    if (!nuevaContrasena || nuevaContrasena.length < 4) {
      alert("La nueva contraseña debe tener al menos 4 caracteres.");
      return;
    }

    fetch(`http://127.0.0.1:5000/usuarios/${usuarioActual.usuario}/contrasena`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nueva_contrasena: nuevaContrasena })
    })
    .then(response => response.json())
    .then(data => {
      alert(data.message || "Contraseña actualizada.");
      document.getElementById("nuevaContrasena").value = "";
      const modal = bootstrap.Modal.getInstance(document.getElementById("modalCambiarContrasena"));
      modal.hide();
    })
    .catch(error => {
      console.error("Error al actualizar la contraseña:", error);
      alert("Hubo un error al intentar cambiar la contraseña.");
    });
  });
});
