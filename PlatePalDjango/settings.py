"""
Django settings for PlatePalDjango project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from typing import Any, Dict, List
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-600#z0+x_1z_!6ki*-h7xf#t71%%1^i7m0q4wxm21!ign%5&25'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_ALLOW_ALL = False
# CORS_ORIGIN_WHITELIST = (
#   'http://localhost:8000',
# )

ALLOWED_HOSTS = ['plate-pal-97cd0667892d.herokuapp.com', 'localhost', 'platepal.eu', 'www.platepal.eu', 'platepal.eu.']

CSRF_TRUSTED_ORIGINS = ['https://plate-pal-97cd0667892d.herokuapp.com', 'https://platepal.eu', 'https://www.platepal.eu', 'https://platepal.eu.']


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'api.apps.ApiConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'hijack',
    'hijack.contrib.admin',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'hijack.middleware.HijackUserMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'PlatePalDjango.urls'

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

WSGI_APPLICATION = 'PlatePalDjango.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db49ukjrioveda',
        'USER': 'njqcdnhutfygdx',
        'PASSWORD': 'fe6ff6791cef7272819e042052a553a3edd7d94dcdc48ee9438f7932ce508319',
        'HOST': 'ec2-52-50-90-145.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
		# 'POOL_OPTIONS' : {
        #     'POOL_SIZE': 2,
        #     'MAX_OVERFLOW': 2,
        #     'RECYCLE': 24 * 60 * 60
        # }
    }
}

# DATABASES = {  
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'platepal',
#     }
# }


db_from_env = dj_database_url.config(conn_max_age=0)
DATABASES['default'].update(db_from_env)

DATA_UPLOAD_MAX_NUMBER_FIELDS = None

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# BACKBLAZE_CONFIG: Dict[str, Any] = {
#     # however you want to securely retrieve these values
#     "application_key_id": '004e55653b341740000000003',
#     "application_key": 'K004BuUCJAWNVq8vS075Vbg1yWxryu0',
#     "bucket": '5e7505163543bbe384810714',
# }

STORAGES = {
    "default": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"},
    "staticfiles": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"}
    }

AWS_ACCESS_KEY_ID= "004e55653b341740000000003" 
AWS_SECRET_ACCESS_KEY= "K004BuUCJAWNVq8vS075Vbg1yWxryu0"
AWS_S3_REGION_NAME= 'us-west-004'
AWS_S3_ENDPOINT_URL= 'https://s3.us-west-004.backblazeb2.com'
AWS_STORAGE_BUCKET_NAME= 'platepal'



# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    # YOUR SETTINGS
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
	'COMPONENT_SPLIT_REQUEST': True,
}
