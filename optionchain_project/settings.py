import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

SECRET_KEY = 'django-insecure-dummy-key-for-now'
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'optionchain_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'optionchain_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Anthropic keys
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', 'sk-ant-xxxxxxxxxxxx')
SUPER_BRAIN_MODEL = os.environ.get('SUPER_BRAIN_MODEL', 'claude-3-opus-20240229') # using claude 3 opus
SUPER_BRAIN_MAX_TOKENS = int(os.environ.get('SUPER_BRAIN_MAX_TOKENS', 2000))
MEMORY_COMPRESS_THRESHOLD = int(os.environ.get('MEMORY_COMPRESS_THRESHOLD', 5000))

# =============================================================
# PythonAnywhere Production Configuration (500MB Free Tier)
# =============================================================

if 'pythonanywhere' in os.environ.get('HOME', ''):
    # Allowed hosts for production
    ALLOWED_HOSTS = ['udayoption.pythonanywhere.com', 'www.udayoption.pythonanywhere.com', 'localhost', '127.0.0.1']
    
    # Production mode
    DEBUG = False
    
    # Static files (compressed for 500MB limit)
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATIC_URL = '/static/'
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Media files
    MEDIA_ROOT = BASE_DIR / 'media'
    MEDIA_URL = '/media/'
    
    # Security settings
    SECURE_BROWSER_XSS_FILTER = True
    CSRF_TRUSTED_ORIGINS = ['https://udayoption.pythonanywhere.com']
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE = False
    
    # Session settings (use database - saves disk space)
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'
    
    # Caching (in-memory, no disk usage)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'optionchain-cache',
            'OPTIONS': {
                'MAX_ENTRIES': 1000
            }
        }
    }
    
    # Logging (errors only - minimal disk usage)
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': BASE_DIR / 'logs' / 'django.log',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'ERROR',
                'propagate': False,
            },
        },
    }
