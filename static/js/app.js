async function uploadFile() {
  const input = document.getElementById("fileInput");
  const status = document.getElementById("status");

  if (!input.files.length) {
    status.textContent = "Please select a file.";
    return;
  }

  const formData = new FormData();
  formData.append("file", input.files[0]);

  status.textContent = "Uploading...";

  const response = await fetch("/api/upload", {
    method: "POST",
    body: formData
  });

  const result = await response.json();

  if (result.ok) {
    status.textContent =
      `Uploaded: ${result.filename} (${result.rows} rows, ${result.columns} columns)`;
    setTimeout(() => window.location.href = "/dashboard", 500);
  } else {
    status.textContent = result.error || "Upload failed.";
  }
}
