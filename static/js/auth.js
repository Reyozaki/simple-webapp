document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");
  const msg = document.getElementById("loginMessage");
  form.onsubmit = async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    try {
      const res = await fetch("/auth/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ username, password })
      });
      const data = await res.json();
      if (res.ok) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "/static/html/dashboard.html";
      } else {
        msg.textContent = data.detail || "Login failed";
      }
    } catch (err) {
      msg.textContent = "Network error";
    }
  };
});
