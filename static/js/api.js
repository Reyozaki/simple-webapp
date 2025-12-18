async function apiFetch(url, options = {}) {
  const token = localStorage.getItem("token");
  options.headers = options.headers || {};
  if (token) options.headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(url, options);
  if (!res.ok) throw res;
  return res;
}
