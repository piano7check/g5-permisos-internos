document.addEventListener('DOMContentLoaded', function() {
    if (window.djangoMessages && Array.isArray(window.djangoMessages)) {
        window.djangoMessages.forEach(function(msg) {
            var icon = 'info';
            if (msg.level && msg.level.includes('success')) icon = 'success';
            else if (msg.level && msg.level.includes('error')) icon = 'error';
            else if (msg.level && msg.level.includes('warning')) icon = 'warning';
            Swal.fire({
                icon: icon,
                title: msg.text,
                showConfirmButton: false,
                timer: 2500,
                position: 'center',
                toast: false
            });
        });
    }
}); 