function parseJwt(token) {
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch {
    return {};
  }
}

async function loadProfile() {
  const payload = parseJwt(localStorage.getItem("token"));
  const profileContent = document.getElementById("profileContent");

  try {
    const res = await apiFetch(`/user/profile/${payload.sub.trim()}`);
    const data = await res.json();

    profileContent.innerHTML = `
      <p><strong>Name:</strong> ${data.name}</p>
      <p><strong>Role:</strong> ${data.role}</p>
      <p><strong>Address:</strong> ${data.address}</p>
      <p><strong>Contact:</strong> ${data.contact}</p>
      <button id="downloadProfilePdfBtn">Download PDF</button>
    `;

    const btn = document.getElementById("downloadProfilePdfBtn");
    if (btn) btn.addEventListener("click", downloadProfilePdf);

  } catch {
    profileContent.textContent = "Failed to load profile.";
  }
}

async function downloadProfilePdf() {
  const payload = parseJwt(localStorage.getItem("token"));
  const userId = payload.sub?.trim();
  const token = localStorage.getItem("token");

  try {
    const res = await fetch(`/user/pdf?user_id=${userId}`, {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (!res.ok) {
      throw new Error(`Server Error: ${res.status}`);
    }

    const blob = await res.blob();
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "profile.pdf";
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(link.href);

  } catch (err) {
    console.error("Download failed:", err);
    alert("Failed to download PDF.");
  }
}

window.loadProfile = loadProfile;
window.downloadProfilePdf = downloadProfilePdf;
window.parseJwt = parseJwt;

document.addEventListener("DOMContentLoaded", () => {
  loadProfile();
});
