document.addEventListener("DOMContentLoaded", function () {
    // Simuler l'état de connexion (à remplacer par une vérification réelle)
    let isLoggedIn = localStorage.getItem("loggedIn") === "true";

    let loginButton = document.getElementById("login-btn");

    if (isLoggedIn) {
        loginButton.innerHTML = "Mon Profil";
        loginButton.href = "monprofil.html"; // Rediriger vers la page de profil
    } else {
        loginButton.innerHTML = "Se connecter";
        loginButton.href = "seconnecter.html"; // Rediriger vers la page de connexion
    }
});
