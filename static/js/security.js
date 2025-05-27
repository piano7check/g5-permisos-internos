document.addEventListener('DOMContentLoaded', function() {
    // Manejar todos los botones de registro de acceso
    document.querySelectorAll('.record-access').forEach(button => {
        button.addEventListener('click', function() {
            const permissionId = this.dataset.permissionId;
            const accessType = this.dataset.accessType;
            const button = this;
            
            // Deshabilitar el botón y mostrar estado de carga
            button.disabled = true;
            const originalContent = button.innerHTML;
            button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Procesando...';

            // Realizar la petición AJAX
            fetch('/security/record-access/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    permission_id: permissionId,
                    access_type: accessType
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Mostrar notificación de éxito
                    showNotification('Éxito', data.message, 'success');
                    
                    // Actualizar el botón según el nuevo tipo de acceso
                    if (accessType === 'ENTRY') {
                        button.classList.remove('btn-success');
                        button.classList.add('btn-danger');
                        button.dataset.accessType = 'EXIT';
                        button.innerHTML = '<i class="fas fa-sign-out-alt me-1"></i> Registrar Salida';
                    } else {
                        button.classList.remove('btn-danger');
                        button.classList.add('btn-success');
                        button.dataset.accessType = 'ENTRY';
                        button.innerHTML = '<i class="fas fa-sign-in-alt me-1"></i> Registrar Entrada';
                    }

                    // Si estamos en la vista de lista, actualizar la celda de último acceso
                    const row = button.closest('tr');
                    if (row) {
                        const lastAccessCell = row.querySelector('td:nth-child(5)');
                        if (lastAccessCell) {
                            const badge = accessType === 'ENTRY' ? 
                                '<span class="badge bg-success">Entrada</span>' : 
                                '<span class="badge bg-danger">Salida</span>';
                            const now = new Date().toLocaleString('es-BO');
                            lastAccessCell.innerHTML = `${badge}<small class="d-block text-muted">${now}</small>`;
                        }
                    }

                    // Si el permiso se completó, recargar la página
                    if (data.record.permission_status === 'COMPLETED') {
                        setTimeout(() => {
                            window.location.reload();
                        }, 1500);
                    }
                } else {
                    // Mostrar notificación de error
                    showNotification('Error', data.message, 'error');
                    // Restaurar el botón a su estado original
                    button.innerHTML = originalContent;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error', 'Ocurrió un error al procesar la solicitud', 'error');
                // Restaurar el botón a su estado original
                button.innerHTML = originalContent;
            })
            .finally(() => {
                // Habilitar el botón nuevamente
                button.disabled = false;
            });
        });
    });

    // Actualizar filtros automáticamente
    document.querySelectorAll('#filter-form input').forEach(input => {
        input.addEventListener('change', function() {
            document.getElementById('filter-form').submit();
        });
    });
});

// Función para obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Función para mostrar notificaciones
function showNotification(title, message, type) {
    // Crear el toast
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    const bgClass = type === 'success' ? 'bg-success' : 'bg-danger';
    
    toast.innerHTML = `
        <div class="toast-header ${bgClass} text-white">
            <strong class="me-auto">${title}</strong>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Inicializar y mostrar el toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 3000
    });
    bsToast.show();
    
    // Eliminar el toast después de ocultarse
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

// Función para crear el contenedor de toasts si no existe
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
} 