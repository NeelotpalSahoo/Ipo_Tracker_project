// admin_panel/static/admin_panel/js/admin.js

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function () {
    console.log('Admin Panel Loaded');

    // Example: Sidebar toggle
    const toggleBtn = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function () {
            sidebar.classList.toggle('collapsed');
        });
    }

    // Example: Show success message after form submission
    const form = document.getElementById('ipo-form');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault(); // prevent actual submission for demo
            alert('IPO registered successfully!');
            form.reset();
        });
    }

    // Example: Highlight active nav item
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.href === window.location.href) {
            link.classList.add('active');
        }
    });
});
