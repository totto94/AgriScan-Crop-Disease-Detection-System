document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(el => {
            el.style.transition = 'opacity 1s';
            el.style.opacity = '0';
            setTimeout(() => el.remove(), 1000);
        });
    }, 5000);
});