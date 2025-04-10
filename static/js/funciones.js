document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('formRegistro');
    const mensaje = document.getElementById('mensaje');
    const letrasRegex = /^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$/;

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const nombre = document.getElementById('nombre').value.trim();
        const apellido = document.getElementById('apellido').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;

        // Validaciones
        if (!letrasRegex.test(nombre)) {
            e.preventDefault();
            alert('El nombre solo puede contener letras');
            return;
        }
        
        if (!letrasRegex.test(apellido)) {
            e.preventDefault();
            alert('El apellido solo puede contener letras');
            return;
        }

        if (!nombre || !apellido) {
            mostrarMensaje("El nombre y apellido no pueden estar vacíos.", true);
            return;
        }

        const emailRegex = /^[\w.-]+@uab\.edu\.bo$/;
        if (!emailRegex.test(email)) {
            mostrarMensaje("El correo debe terminar en @uab.edu.bo", true);
            return;
        }

        if (password.length < 6) {
            mostrarMensaje("La contraseña debe tener al menos 6 caracteres.", true);
            return;
        }

        // Enviar al backend
        axios.post('/api/registro/', {
            nombre: nombre,
            apellido: apellido,
            email: email,
            password: password
        })
        .then(response => {
            mostrarMensaje("Usuario registrado con éxito.", false);
            setTimeout(() => {
                window.location.href = "/login";  // Redirigir al login
            }, 5000);
        })
        .catch(error => {
            const errMsg = error.response?.data?.error || "Error desconocido.";
            mostrarMensaje(errMsg, true);
        });
    });

    function mostrarMensaje(texto, esError) {
        mensaje.textContent = texto;
        mensaje.style.color = esError ? "red" : "green";
    }
});
