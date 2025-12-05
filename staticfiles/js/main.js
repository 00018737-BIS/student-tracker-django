// static/js/custom.js
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            if (alert) {
                new bootstrap.Alert(alert).close();
            }
        });
    }, 5000);

    // Add loading spinner to forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Saving...';
                submitBtn.disabled = true;
            }
        });
    });

    // Toast notification for success
    if (document.querySelector('.alert-success')) {
        const toast = new bootstrap.Toast({
            template: `<div class="toast align-items-center text-white bg-success border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="fas fa-check-circle"></i> Action completed successfully!
                    </div>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
                </div>
            </div>`
        });
        toast.show();
    }
});