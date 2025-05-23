class AccessRegister {
    constructor() {
        this.toast = new bootstrap.Toast(document.getElementById('toast'));
        this.form = document.getElementById('accessForm');
        this.recentRecords = document.getElementById('recentRecords');
        this.recordAccessUrl = this.form.dataset.recordAccessUrl;
        this.accessHistoryUrl = this.form.dataset.accessHistoryUrl;
        this.setupEventListeners();
        this.loadRecentRecords();
    }

    setupEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        const formData = {
            resident_id: document.getElementById('resident').value,
            access_type: document.querySelector('input[name="access_type"]:checked')?.value,
            notes: document.getElementById('notes').value
        };

        try {
            const response = await this.recordAccess(formData);
            const data = await response.json();
            
            if (response.ok) {
                this.addRecordToTable(data.record);
                this.showNotification(data.message, 'success');
                this.form.reset();
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            this.showNotification(error.message || 'Error al registrar el acceso', 'danger');
        }
    }

    async recordAccess(formData) {
        return await fetch(this.recordAccessUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(formData)
        });
    }

    addRecordToTable(record) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${record.resident_name}</td>
            <td>
                <span class="badge ${record.access_type === 'Entrada' ? 'bg-success' : 'bg-danger'}">
                    ${record.access_type}
                </span>
            </td>
            <td>${record.timestamp}</td>
        `;
        this.recentRecords.insertBefore(row, this.recentRecords.firstChild);
    }

    showNotification(message, type) {
        const toastHeader = document.querySelector('.toast-header');
        toastHeader.className = 'toast-header'; // Reset classes
        toastHeader.classList.add(`bg-${type}`, 'text-white');
        document.querySelector('.toast-body').textContent = message;
        this.toast.show();
    }

    async loadRecentRecords() {
        try {
            const response = await fetch(this.accessHistoryUrl);
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const records = Array.from(doc.querySelectorAll('tbody tr')).slice(0, 5);
            this.recentRecords.innerHTML = records.map(record => record.outerHTML).join('');
        } catch (error) {
            console.error('Error loading recent records:', error);
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new AccessRegister();
}); 