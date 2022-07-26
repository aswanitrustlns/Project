"""
Django settings for TrustCRM project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x98$y6+al)ej+^0$jq99v%uwi31@)(ctb!deq#6qtq$j*w2lz%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',   
    'Admin',
    'Backoffice',
    'CRF',
    'Automation',
    'rest_framework'
    
    
]

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#     'file': {
#         'level': 'DEBUG',
#         'class': 'logging.FileHandler',
#         'filename': os.path.join(BASE_DIR,'Trust.log'),
#         },
#     },
#     'loggers': {
#     'django': {
#         'handlers': ['file'],
#         'level': 'DEBUG',
#         'propagate': True,
#         },
#     },
# }
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TrustCRM.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Admin.context_processors.get_sales_performers',
                
            ],
        },
    },
]

WSGI_APPLICATION = 'TrustCRM.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'mssql',
    #     'NAME': 'SVGTcCRM20220926',
    #     'USER': 'tinstcrm',
    #     'PASSWORD': 'Trust_2021',
    #     'HOST': '213.175.205.19',
    #     'PORT': '1433',
    #      'OPTIONS': {
    #         'driver': 'ODBC Driver 17 for SQL Server',
    #     },
    # },
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'TCCRM_SYC',
        'USER': 'TCSCRM',
        'PASSWORD': 'TCSY@22!!',
        'HOST': '185.4.178.134',
        'PORT': '1433',
         'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
    'seychelles': {
        'ENGINE': 'mssql',
        'NAME': 'TCCRM_SYC',
        'USER': 'TCSCRM',
        'PASSWORD': 'TCSY@22!!',
        'HOST': '185.4.178.134',
        'PORT': '1433',
         'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
    'ib': {
        'ENGINE': 'mssql',
        'NAME': 'CyTcCRM',
        'USER': 'cycrm',
        'PASSWORD': 'B7TcxNTdQVZaVG22puzr',
        'HOST': '213.7.196.98',
        'PORT': '1433',
         'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
       'crf': {
        'ENGINE': 'mssql',
        'NAME': 'CRF',
        'USER': 'TCSCRM',
        'PASSWORD': 'TCSY@22!!',
        'HOST': '185.4.178.134',
        'PORT': '1433',
         'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
     'svg': {
        'ENGINE': 'mssql',
        'NAME': 'TCCRMClientarea_SYC',
        'USER': 'TCSCRM',
        'PASSWORD': 'TCSY@22!!',
        'HOST': '185.4.178.134',
        'PORT': '1433',
         'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SESSION_COOKIE_AGE=3600

SESSION_EXPIRE_SECONDS = 3600

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

X_FRAME_OPTIONS = 'SAMEORIGIN'

# SESSION_TIMEOUT_REDIRECT = '/accounts/logout/' 

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
# STATIC_ROOT = (os.path.join(BASE_DIR, "static"))

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_ROOT=(os.path.join(BASE_DIR, "uploads"))
  
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL='/media/'
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'euk-110535.eukservers.com'
EMAIL_USE_TSL=False
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = 'cs@trustcapital.com'
EMAIL_HOST_PASSWORD = 'CT16ca20sa'
DEFAULT_FROM_EMAIL ='Trust Capital cs@trustcapital.com'
