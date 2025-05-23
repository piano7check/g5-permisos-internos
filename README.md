# Sistema de Gestión de Permisos Internos

Sistema web para la gestión de permisos internos y control de accesos.

## Características

- Gestión de permisos (solicitud, aprobación, rechazo)
- Control de accesos (entradas/salidas)
- Autenticación con email y Google
- Roles de usuario (residentes, encargados, seguridad, admin)
- Auditoría de acciones
- Notificaciones por email

## Requisitos

- Python 3.8+
- MySQL 8.0+
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd g5-permisos-internos
```

2. Crear y activar entorno virtual:
```bash
python -m venv env
# En Windows:
env\Scripts\activate
# En Linux/Mac:
source env/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
- Copiar `.env.example` a `.env`
- Editar `.env` con tus configuraciones

5. Crear base de datos MySQL:
```sql
CREATE DATABASE db_permisos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. Aplicar migraciones:
```bash
python manage.py migrate
```

7. Crear superusuario:
```bash
python manage.py createsuperuser
```

8. Recopilar archivos estáticos:
```bash
python manage.py collectstatic
```

## Configuración

### Variables de Entorno (.env)

```plaintext
# Django settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True

# Database settings
DB_NAME=db_permisos
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=3306

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Google OAuth2 settings
SOCIAL_AUTH_GOOGLE_CLIENT_ID=your-client-id
SOCIAL_AUTH_GOOGLE_SECRET=your-client-secret
```

### Google OAuth2

1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear un nuevo proyecto
3. Habilitar Google+ API
4. Configurar pantalla de consentimiento
5. Crear credenciales OAuth2
6. Agregar URLs de redirección:
   - http://localhost:8000/accounts/google/login/callback/
   - http://your-domain.com/accounts/google/login/callback/

## Desarrollo

1. Activar entorno virtual:
```bash
env\Scripts\activate  # Windows
source env/bin/activate  # Linux/Mac
```

2. Iniciar servidor de desarrollo:
```bash
python manage.py runserver
```

3. Acceder a:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/admin/

## Estructura del Proyecto

```
g5-permisos-internos/
├── a_authentication/  # Autenticación personalizada
├── a_users/          # Gestión de usuarios
├── a_permissions/    # Gestión de permisos
├── a_security/       # Control de accesos
├── a_audit/         # Sistema de auditoría
├── static/          # Archivos estáticos
│   ├── css/
│   ├── js/
│   └── img/
└── templates/       # Templates HTML
```

## Contribuir

1. Crear rama para nueva característica
2. Hacer commit de cambios
3. Crear pull request

## Licencia

Este proyecto está bajo la licencia MIT.

