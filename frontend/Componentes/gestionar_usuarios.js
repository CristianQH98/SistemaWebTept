document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("formAgregarUsuario");
  const tabla = document.getElementById("tablaUsuarios");
  const btnGuardar = document.getElementById("btnGuardarUsuario");
  const btnCancelar = document.getElementById("btnCancelarEdicion");
  const modoEdicion = document.getElementById("modoEdicion");
  const campos = ['nombre', 'apellido', 'usuario', 'contrasena', 'rol', 'estado'];

  cargarUsuarios();

  campos.forEach(id => {
    const campo = document.getElementById(id);
    if (campo) {
      campo.addEventListener('input', () => validarCampoIndividual(id));
    }
  });

  btnCancelar.addEventListener("click", () => {
    form.reset();
    delete form.dataset.editUsuario;
    modoEdicion.classList.add('d-none');
    btnCancelar.style.display = 'none';
    btnGuardar.textContent = 'Agregar Usuario';
    limpiarErrores();
  });

  function mostrarError(mensaje, campoId = null) {
    let errorDiv = document.getElementById('errorMensaje');
    if (!errorDiv) {
      errorDiv = document.createElement('div');
      errorDiv.id = 'errorMensaje';
      errorDiv.className = 'alert alert-danger mt-2';
      form.prepend(errorDiv);
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

    campos.forEach(id => {
      const campo = document.getElementById(id);
      campo.classList.remove('is-invalid');
      const fb = document.getElementById(`${id}-feedback`);
      if (fb) fb.remove();
    });
  }

  function validarCampoIndividual(campoId) {
    const valor = document.getElementById(campoId).value.trim();
    const soloLetras = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$/;
    const soloAlfanumerico = /^[a-zA-Z0-9]+$/;

    let valido = true;
    let mensaje = '';

    switch (campoId) {
      case 'nombre':
      case 'apellido':
        valido = soloLetras.test(valor) && valor.length >= 2;
        mensaje = 'Solo letras, mínimo 2 caracteres';
        break;
      case 'usuario':
        valido = soloAlfanumerico.test(valor) && valor.length >= 3;
        mensaje = 'Solo letras y números, mínimo 3 caracteres';
        break;
      case 'contrasena':
        valido = valor.length >= 4;
        mensaje = 'Mínimo 4 caracteres';
        break;
      case 'rol':
        valido = ['psicologo', 'administrador'].includes(valor);
        mensaje = 'Rol inválido';
        break;
      case 'estado':
        valido = ['activo', 'inactivo'].includes(valor);
        mensaje = 'Estado inválido';
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

    return valido;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    limpiarErrores();

    const nuevoUsuario = {
      nombre: document.getElementById("nombre").value.trim(),
      apellido: document.getElementById("apellido").value.trim(),
      usuario: document.getElementById("usuario").value.trim(),
      contraseña: document.getElementById("contrasena").value.trim(),
      rol: document.getElementById("rol").value,
      estado: document.getElementById("estado").value,
      fecha_creacion: new Date().toISOString().split("T")[0]
    };

    let todoOk = true;
    campos.forEach(id => {
      if (!validarCampoIndividual(id)) todoOk = false;
    });

    if (!todoOk) return;

    const editUsuario = form.dataset.editUsuario;

    try {
      const response = await fetch(editUsuario ? `http://127.0.0.1:5000/usuarios/${editUsuario}` : "http://127.0.0.1:5000/usuarios", {
        method: editUsuario ? "PUT" : "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(nuevoUsuario)
      });

      const data = await response.json();
      if (response.ok) {
        alert(editUsuario ? "Usuario actualizado." : "Usuario creado exitosamente.");
        form.reset();
        delete form.dataset.editUsuario;
        btnGuardar.textContent = 'Agregar Usuario';
        modoEdicion.classList.add('d-none');
        btnCancelar.style.display = 'none';
        limpiarErrores();
        cargarUsuarios();
      } else {
        mostrarError(data.error || "Error en la operación.");
      }
    } catch (err) {
      console.error("Error:", err);
      mostrarError("No se pudo conectar al servidor.");
    }
  });

  async function cargarUsuarios() {
    try {
      const response = await fetch("http://127.0.0.1:5000/usuarios");
      const usuarios = await response.json();

      tabla.innerHTML = "";

      usuarios.forEach((user) => {
        const fila = document.createElement("tr");
        fila.innerHTML = `
          <td>${user.id || "—"}</td>
          <td>${user.nombre}</td>
          <td>${user.apellido}</td>
          <td>${user.usuario}</td>
          <td>${user.rol}</td>
          <td>${user.estado}</td>
          <td>${user.fecha_creacion || "—"}</td>
          <td>
            <button class="btn btn-warning btn-sm" onclick="editarUsuario('${user.usuario}')">Editar</button>
            <button class="btn btn-danger btn-sm" onclick="eliminarUsuario('${user.usuario}')">Eliminar</button>
          </td>
        `;
        tabla.appendChild(fila);
      });
    } catch (err) {
      console.error("Error al obtener usuarios:", err);
      mostrarError("No se pudieron cargar los usuarios.");
    }
  }

  window.editarUsuario = function (usuarioId) {
    const fila = [...tabla.rows].find(r => r.cells[3].textContent === usuarioId);
    if (!fila) return;

    document.getElementById("nombre").value = fila.cells[1].textContent;
    document.getElementById("apellido").value = fila.cells[2].textContent;
    document.getElementById("usuario").value = fila.cells[3].textContent;
    document.getElementById("rol").value = fila.cells[4].textContent;
    document.getElementById("estado").value = fila.cells[5].textContent;
    document.getElementById("contrasena").value = ""; // No se puede recuperar contraseña

    form.dataset.editUsuario = usuarioId;
    btnGuardar.textContent = 'Guardar Cambios';
    btnCancelar.style.display = 'inline-block';
    modoEdicion.classList.remove('d-none');
  }

  window.eliminarUsuario = async function (usuario) {
    if (!confirm(`¿Deseas eliminar al usuario "${usuario}"?`)) return;

    try {
      const response = await fetch(`http://127.0.0.1:5000/usuarios/${usuario}`, {
        method: "DELETE"
      });

      const data = await response.json();
      if (response.ok) {
        alert("Usuario eliminado.");
        cargarUsuarios();
      } else {
        mostrarError(data.error || "Error al eliminar usuario.");
      }
    } catch (err) {
      console.error("Error al eliminar:", err);
      mostrarError("No se pudo conectar al servidor.");
    }
  }
});
