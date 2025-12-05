document.addEventListener("DOMContentLoaded", function () {
  const alerts = document.querySelectorAll(".alert-dismissible");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });

  const uploadForms = document.querySelectorAll(
    'form[enctype="multipart/form-data"]'
  );
  uploadForms.forEach(function (form) {
    form.addEventListener("submit", function (e) {
      const fileInput = form.querySelector('input[type="file"]');
      if (fileInput && !fileInput.files.length) {
        e.preventDefault();
        alert("Please select a file to upload.");
        return false;
      }
    });
  });

  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach(function (input) {
    input.addEventListener("change", function () {
      const fileName = this.files[0]?.name;
      const label = this.nextElementSibling;
      if (fileName && label && label.classList.contains("form-text")) {
        label.textContent = "Selected: " + fileName;
      }
    });
  });

  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
});
