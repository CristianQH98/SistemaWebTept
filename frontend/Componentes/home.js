// Validar sesión y mostrar panel según rol
const rawData = localStorage.getItem("usuarioActual");

if (!rawData) {
    alert("Sesión inválida. Cerrando sesión.");
    window.location.href = "login.html";
} else {
    const usuario = JSON.parse(rawData);
    const rol = usuario?.rol?.toLowerCase();

    if (rol === "administrador") {
        document.getElementById("soloAdmin").style.display = "block";
    } else if (rol === "psicologo") {
        document.getElementById("soloPsico").style.display = "block";
    } else {
        alert("Rol no definido o inválido. Cerrando sesión por seguridad.");
        localStorage.removeItem("usuarioActual");
        window.location.href = "login.html";
    }
}