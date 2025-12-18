function logout() {
  localStorage.removeItem("token");
  window.location.href = "/static/html/login.html";
}

document.addEventListener("DOMContentLoaded", () => {
  if (!localStorage.getItem("token")) {
    logout();
    return;
  }

  const payload = parseJwt(localStorage.getItem("token"));

  const profileTab = document.getElementById("profileTab");
  const usersTab = document.getElementById("usersTab");
  const logoutBtn = document.getElementById("logoutBtn");

  if (payload.scope !== "admin") usersTab.style.display = "none";

  profileTab.onclick = () => showTab("profile");
  usersTab.onclick = () => showTab("users");
  logoutBtn.onclick = logout;

  function showTab(tabId) {
    document.querySelectorAll(".tab").forEach(t => t.style.display = "none");
    document.getElementById(tabId).style.display = "block";
    if (tabId === "profile") loadProfile();
    if (tabId === "users") {
      loadUsers(1);
      initCreateUserForm();
    }
  }

  showTab("profile");
});
