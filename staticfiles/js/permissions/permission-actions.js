class PermissionActions {
    constructor() {
        this.rejectModal = new bootstrap.Modal(document.getElementById('rejectModal'));
        this.setupEventListeners();
    }

    setupEventListeners() {
        document.querySelectorAll('[data-action="approve"]').forEach(button => {
            button.addEventListener('click', (e) => this.handleApprove(e));
        });

        document.querySelectorAll('[data-action="reject"]').forEach(button => {
            button.addEventListener('click', (e) => this.handleRejectClick(e));
        });

        document.getElementById('confirmReject')?.addEventListener('click', () => this.handleRejectSubmit());
    }

    async handleApprove(e) {
        const permissionId = e.currentTarget.dataset.permissionId;
        if (!confirm('¿Estás seguro de que deseas aprobar este permiso?')) return;

        try {
            const response = await this.approvePermission(permissionId);
            if (response.ok) {
                window.location.reload();
            } else {
                const data = await response.json();
                alert(data.message || 'Error al aprobar el permiso');
            }
        } catch (error) {
            alert('Error al procesar la solicitud');
        }
    }

    handleRejectClick(e) {
        this.currentPermissionId = e.currentTarget.dataset.permissionId;
        this.rejectModal.show();
    }

    async handleRejectSubmit() {
        const reason = document.getElementById('rejection_reason').value;
        if (!reason) {
            alert('Por favor, ingresa el motivo del rechazo');
            return;
        }

        try {
            const response = await this.rejectPermission(this.currentPermissionId, reason);
            if (response.ok) {
                this.rejectModal.hide();
                window.location.reload();
            } else {
                const data = await response.json();
                alert(data.message || 'Error al rechazar el permiso');
            }
        } catch (error) {
            alert('Error al procesar la solicitud');
        }
    }

    async approvePermission(permissionId) {
        return await fetch(`/permissions/${permissionId}/approve/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        });
    }

    async rejectPermission(permissionId, reason) {
        return await fetch(`/permissions/${permissionId}/reject/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({ rejection_reason: reason })
        });
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new PermissionActions();
}); 