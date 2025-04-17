document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('formRegistro');
    const mensaje = document.getElementById('mensaje');
    const letrasRegex = /^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$/;
    const emailRegex = /^[\w.-]+@uab\.edu\.bo$/;

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const nombre = document.getElementById('first_name').value.trim();
        const apellido = document.getElementById('last_name').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;

        if (!nombre || !apellido || !email || !password) {
            mostrarMensaje("Todos los campos son obligatorios.", true);
            return;
        }

        if (!letrasRegex.test(nombre)) {
            mostrarMensaje("El nombre solo puede contener letras.", true);
            return;
        }

        if (!letrasRegex.test(apellido)) {
            mostrarMensaje("El apellido solo puede contener letras.", true);
            return;
        }

        if (!emailRegex.test(email)) {
            mostrarMensaje("El correo debe terminar en @uab.edu.bo", true);
            return;
        }

        if (password.length < 6) {
            mostrarMensaje("La contraseña debe tener al menos 6 caracteres.", true);
            return;
        }

        axios.post('/api/registro/', {
            first_name: nombre,
            last_name: apellido,
            email: email,
            password: password
        })
        .then(response => {
            mostrarMensaje("✅ Usuario registrado con éxito.", false);
            setTimeout(() => {
                window.location.href = "/login";
            }, 3000);
        })
        .catch(error => {
            const data = error.response?.data;
            let mensajeError = "Error desconocido.";

            if (typeof data === 'object') {
                if (data.non_field_errors) {
                    mensajeError = data.non_field_errors[0];
                } else {
                    for (let campo in data) {
                        mensajeError = data[campo][0];
                        break;
                    }
                }
            }

            mostrarMensaje("❌ " + mensajeError, true);
        });
    });

    function mostrarMensaje(texto, esError) {
        mensaje.textContent = texto;
        mensaje.style.color = esError ? "red" : "green";
    }
});
