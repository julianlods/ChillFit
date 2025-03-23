from pathlib import Path
import os

# Rutas base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de seguridad
SECRET_KEY = 'django-insecure-...'
DEBUG = True
ALLOWED_HOSTS = []

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ChillFit',
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de rutas principales
ROOT_URLCONF = 'Proyecto1.urls'

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'ChillFit' / 'templates'],  # Ajusta según tu estructura
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuración de WSGI
WSGI_APPLICATION = 'Proyecto1.wsgi.application'

# Configuración de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configuración de idioma y zona horaria
LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Configuración de archivos estáticos
STATIC_URL = '/static/'

# Campo automático por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración del modelo de usuario personalizado
AUTH_USER_MODEL = 'ChillFit.Usuario'

# Configuración de rutas de login/logout
LOGIN_URL = 'login'  # Nombre de la vista de inicio de sesión
LOGOUT_REDIRECT_URL = 'login'  # Redirección después de cerrar sesión
LOGIN_REDIRECT_URL = 'home'  # Cambia 'home' por el nombre de la vista donde deseas redirigir

# Backends de autenticación
AUTHENTICATION_BACKENDS = [
    'ChillFit.backends.UsuarioEmailBackend',  # Backend personalizado
    'django.contrib.auth.backends.ModelBackend',  # Backend por defecto
]

# Configuración del servidor de correo para desarrollo
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# **Configuración de MercadoPago**
# Credenciales de MercadoPago
MERCADOPAGO_PUBLIC_KEY = "TEST-1b836d74-15b0-459d-aeb5-b5aba3beec2d"
MERCADOPAGO_ACCESS_TOKEN = "TEST-3666286772975422-032019-8fbe3321bf183c57c2935fa546d4237d-281041896"


