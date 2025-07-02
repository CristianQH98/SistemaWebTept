document.addEventListener("DOMContentLoaded", function () {
    const usuario = JSON.parse(localStorage.getItem("usuarioActual"));

    if (!usuario || usuario.rol !== "administrador") {
        alert("Acceso restringido: solo para administradores");
        window.location.href = "home.html";
        return;
    }

    document.getElementById("nombre-admin").textContent = usuario.nombre;
    document.getElementById("apellido-admin").textContent = usuario.apellido;
    document.getElementById("usuario-admin").textContent = usuario.usuario;

    const btnGestion = document.getElementById("btn-gestionar-usuarios");
    if (btnGestion) {
        btnGestion.addEventListener("click", () => {
            window.location.href = "gestionar_usuarios.html";
        });
    }
});
