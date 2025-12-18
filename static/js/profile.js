function parseJwt(token) {
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch {
    return {};
  }
}

function isValidUUID(uuid) {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(uuid);
}

async function loadProfile() {
  const payload = parseJwt(localStorage.getItem("token"));
  const profileContent = document.getElementById("profileContent");

  if (!payload.sub) {
    profileContent.textContent = "Invalid token. User ID missing.";
    return;
  }

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

  if (!userId) {
    alert("User ID missing");
    return;
  }

  const token = localStorage.getItem("token");

  const res = await fetch(`/user/profile/pdf?user_id=${userId}`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  if (!res.ok) {
    const err = await res.text();
    console.error("PDF download failed:", err);
    alert("Failed to download PDF");
    return;
  }

  const blob = await res.blob();
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "profile.pdf";
  document.body.appendChild(link);
  link.click();
  link.remove();
}

window.loadProfile = loadProfile;
window.downloadProfilePdf = downloadProfilePdf;
window.parseJwt = parseJwt;

document.addEventListener("DOMContentLoaded", () => {
  loadProfile();
});
