"""
Django settings for projeto1 project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from django.contrib.messages import constants as messages
from pathlib import Path
import envconfiguration as config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.DJANGO_SECRET_KEY #type: ignore

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.DJANGO_DEBUG #type: ignore

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://*.cett.org.br',
    'http://*.cett.org.br',
    'https://*.cett.dev.br',
    'http://*.cett.dev.br',
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appprojeto1',
    'SolicitacaoDeTurmas.apps.SolicitacaodeturmasConfig',
    'DivisaoDeMetas.apps.DivisaodemetasConfig',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_tables2',
    'django_filters',
    'bootstrap5',
    'django_bootstrap_icons',
    'fontawesome_5',
    'aprovaedital',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

ROOT_URLCONF = 'projeto1.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


WSGI_APPLICATION = 'projeto1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.CAMUNDA_DOMAINS_DB,  # type: ignore
        'USER': config.CAMUNDA_DOMAINS_USER,  # type: ignore
        'HOST': config.CAMUNDA_DOMAINS_HOST,  # type: ignore
        'PASSWORD': config.CAMUNDA_DOMAINS_PASS,  # type: ignore
        'PORT': config.CAMUNDA_DOMAINS_PORT,  # type: ignore

        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"}
    },
}

# DATABASE_ROUTERS = ['appprojeto1.dbrotas.EixosRota','appprojeto1.dbrotas.CamundaRota']

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

USE_L10N = True

DATE_FORMAT = '%Y-%m-%d'
DATE_INPUT_FORMATS = '%Y-%m-%d'
DATETIME_INPUT_FORMATS = ['%Y-%m-%d']
USE_THOUSAND_SEPARATOR = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
