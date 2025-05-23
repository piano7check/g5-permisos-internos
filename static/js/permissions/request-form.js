class PermissionRequestForm {
    constructor() {
        this.setupDateValidation();
    }

    setupDateValidation() {
        const today = new Date().toISOString().split('T')[0];
        
        // Establecer fecha mínima como hoy
        document.querySelectorAll('input[type="datetime-local"]').forEach(input => {
            input.min = today + 'T00:00';
        });

        // Validar que la fecha de fin sea posterior a la de inicio
        document.getElementById('end_date')?.addEventListener('change', (e) => {
            const startDate = document.getElementById('start_date').value;
            const endDate = e.target.value;
            
            if (startDate && endDate && startDate > endDate) {
                alert('La fecha de fin debe ser posterior a la fecha de inicio');
                e.target.value = '';
            }
        });

        // Validar que la fecha de inicio sea posterior a hoy
        document.getElementById('start_date')?.addEventListener('change', (e) => {
            const selectedDate = new Date(e.target.value);
            const now = new Date();
            
            if (selectedDate < now) {
                alert('La fecha de inicio debe ser posterior a la fecha actual');
                e.target.value = '';
            }
        });
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new PermissionRequestForm();
}); 