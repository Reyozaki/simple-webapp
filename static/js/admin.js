let currentPage = 1;
let editingUserId = null;
let currentFilterAddress = "";

document.addEventListener("DOMContentLoaded", () => {
  initCreateUserForm();

  document
    .getElementById("searchUsersBtn")
    .addEventListener("click", () => {
      currentFilterAddress =
        document.getElementById("addressFilter").value.trim();
      loadUsers(1);
    });

  const downloadBtn = document.getElementById("downloadUsersPdfBtn");
  if (downloadBtn) {
    downloadBtn.addEventListener("click", downloadUsersPdf);
  }

  loadUsers(1);
});

function isValidEmail(email) {
  return /^(([a-zA-Z0-9\._]+)[@]([a-zA-Z0-9]+)[\.]([a-z]{2,3}))$/.test(email);
}

function showError(msgEl, message) {
  msgEl.style.color = "red";
  msgEl.textContent = message;
}

function loadUsers(page = 1) {
  currentPage = page;

  const params = new URLSearchParams({
    page,
    size: 5
  });

  if (currentFilterAddress) {
    params.append("filter_address", currentFilterAddress);
  }

  apiFetch(`/admin/users?${params.toString()}`)
    .then(r => r.json())
    .then(([paginationData, meta]) => {
      renderUsers(paginationData.items);
      renderPagination(paginationData.page, paginationData.total_page);

      document.getElementById("totalUsers").textContent =
        `Total results: ${meta.total}`;
    });
}

function renderUsers(users) {
  const container = document.getElementById("userList");
  container.innerHTML = `
    <table border="1" cellpadding="5">
      <tr>
        <th>Name</th>
        <th>Role</th>
        <th>Address</th>
        <th>Contact</th>
        <th>Actions</th>
      </tr>
      ${users.map(u => `
        <tr>
          <td>${u.name}</td>
          <td>${u.role}</td>
          <td>${u.address ?? ""}</td>
          <td>${u.contact ?? ""}</td>
          <td>
            <button onclick="editUser('${u.id}')">Update</button>
            <button onclick="deleteUser('${u.id}')">Delete</button>
          </td>
        </tr>
      `).join("")}
    </table>
  `;
}

function renderPagination(page, totalPages) {
  const container = document.getElementById("pagination");
  container.innerHTML = "";
  for (let i = 1; i <= totalPages; i++) {
    container.innerHTML += `
      <button onclick="loadUsers(${i})" ${i === page ? "disabled" : ""}>
        ${i}
      </button>
    `;
  }
}

function deleteUser(userId) {
  if (!confirm("Are you sure you want to delete this user?")) return;
  apiFetch(`/admin/delete-user?user_id=${userId}`, { method: "DELETE" })
    .then(r => r.json())
    .then(() => loadUsers(currentPage));
}

function editUser(userId) {
  editingUserId = userId;
  apiFetch(`/admin/users?page=1&size=100`)
    .then(r => r.json())
    .then(([paginationData]) => {
      const user = paginationData.items.find(u => u.id === userId);
      if (!user) return;

      document.getElementById("userId").value = user.id;
      const nameParts = user.name.split(" ");
      document.getElementById("fname").value = nameParts[0];
      document.getElementById("lname").value = nameParts[1] || "";
      document.getElementById("username").value = user.username || "";
      document.getElementById("role").value = user.role || "";
      document.getElementById("address").value = user.address || "";
      document.getElementById("contact").value = user.contact || "";
      document.getElementById("password").value = "";
    });
}

function initCreateUserForm() {
  const form = document.getElementById("createUserForm");
  const msg = document.getElementById("message");

  form.onsubmit = async (e) => {
    e.preventDefault();

    const msg = document.getElementById("message");

    const userId = document.getElementById("userId").value || null;
    const fname = document.getElementById("fname").value.trim();
    const lname = document.getElementById("lname").value.trim();
    const username = document.getElementById("username").value.trim();
    const role = document.getElementById("role").value.trim();
    const address = document.getElementById("address").value.trim();
    const contact = document.getElementById("contact").value.trim();
    const password = document.getElementById("password").value;

    if (username.length < 4) {
      return showError(msg, "Username must be at least 4 characters long.");
    }

    if (!userId && (!password || password.length < 6)) {
      return showError(msg, "Password must be at least 6 characters long.");
    }

    if (password && password.length < 6) {
      return showError(msg, "Password must be at least 6 characters long.");
    }

    if (contact && !isValidEmail(contact)) {
      return showError(msg, "Email must be in format example@mail.com.");
    }

    if (!fname || !lname || !role) {
      return showError(msg, "First name, last name, and role are required.");
    }

    const data = {
      fname,
      lname,
      username,
      role,
      address,
      contact
    };

    if (password) {
      data.password = password;
    }

    try {
      let url = "/admin/create-user";
      let method = "POST";
  
      if (userId) {
        url = `/admin/update-user?user_id=${userId}`;
        method = "PATCH";
      }

      const res = await apiFetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      const result = await res.json();
      msg.style.color = res.ok ? "green" : "red";
      msg.textContent = res.ok ? result.message : result.detail || "Error";

      if (res.ok) {
        form.reset();
        document.getElementById("userId").value = "";
        editingUserId = null;
        loadUsers(currentPage);
      }

    } catch {
      showError(msg, "Network error");
    }
  };
}

function downloadUsersPdf() {
  downloadPdf("/admin/users/pdf", "users.pdf");
}

window.loadUsers = loadUsers;
window.deleteUser = deleteUser;
window.editUser = editUser;
window.initCreateUserForm = initCreateUserForm;
window.downloadUsersPdf = downloadUsersPdf;
