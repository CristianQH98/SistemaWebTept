
function configurarPerfilLink() {
  const perfilLink = document.getElementById("perfilLink");
  const rawData = localStorage.getItem("usuarioActual");

  if (perfilLink && rawData) {
    try {
      const usuario = JSON.parse(rawData);
      const rol = usuario?.rol?.toLowerCase();

      if (rol === "administrador") {
        perfilLink.href = "perfil_admin.html";
      } else if (rol === "psicologo") {
        perfilLink.href = "perfil.html";
      } else {
        perfilLink.href = "login.html";
      }
    } catch (e) {
      perfilLink.href = "login.html";
    }
  }
}
