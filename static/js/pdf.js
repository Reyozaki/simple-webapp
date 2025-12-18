async function downloadPdf(url, filename) {
  const res = await apiFetch(url);
  const blob = await res.blob();
  const link = document.createElement("a");
  link.href = window.URL.createObjectURL(blob);
  link.download = filename;
  link.click();
}
