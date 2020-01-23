"""
Django settings for ufts ufts.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from socket import gethostname, gethostbyname
from logging.handlers import SysLogHandler
import logging

# from termsandconditions.decorators import terms_required

# Build paths inside the ufts like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWNER = 'Jim Lamb'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n9ucrt9=)e!d=(uaimum@7onn%uvua6a(m^9-=zmscd$&f%(%u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
FROM_EMAIL = 'ufts_noreply@example.com'

ALLOWED_HOSTS = ['support.atcii.net','172.16.16.125','support.atcii.net', 'patches.atcii.net', '35.231.90.209','ufts-demo.atcii.net', 'www.atcii.net', '127.0.0.1', 'greenlan.net',]
# secure proxy SSL header and secure cookies
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# session expire at browser close
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# wsgi scheme
os.environ['wsgi.url_scheme'] = 'https'

# Application definition


DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'django_classification_banner',
    'request',
    'chosen',
    'compressor',
    'crispy_forms',
]

PROJECT_APPS = [
    'about.apps.AboutConfig',
    'dayone.apps.DayoneConfig',
    'documentation.apps.DocumentationConfig',
    'jsa.apps.JsaConfig',
    'uploads.apps.UploadsConfig',
    'users.apps.UsersConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'request.middleware.RequestMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ufts.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django_classification_banner.context_processors.classification',
                'uploads.context_processors.global_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'ufts.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# if DEBUG:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': 'ufts',
#             'USER': 'uftsuser',
#             'PASSWORD': 'Th!sI5aS3cr3t',
#             'HOST': 'localhost',
#             'PORT': '5432',
#         }
#     }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
COMPRESS_PRECOMPILERS = (('text/x-scss', 'django_libsass.SassCompiler'),)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'


LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

CLASSIFICATION_TEXT = 'Unclassified//FOUO'
CLASSIFICATION_TEXT_COLOR = 'black'
CLASSIFICATION_BACKGROUND_COLOR = 'green'
# CLASSIFICATION_LINK = '/security'

PRODUCT_NAME = 'UFTS'
OWNER = 'James Lamb'
LICENSE_KEY = 'CBXS-V9K7-9CRR-PLU6-1LN4'
ACCESS_CODE = '1863'
COMPANY_NAME = 'Juniper Networks'
COMPANY_ADDRESS = '2251 Corporate Park Dr #100, Herndon, VA 20171'
COMPANY_PHONE = '(571) 203-1700'
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
THUMB_SIZE = (400, 400)
AUTH_USER_MODEL = 'users.CustomUser'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
# Logging to console, syslog and file
#
# Logging to console, syslog and file
#
# if DEBUG:

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(process)-5d %(thread)d %(module)s %(name)-20s %(levelname)-8s %(message)s'

        },
        'simple': {
            'format': '[%(asctime)s]  %(name)s %(levelname)s %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
        },
        'app-logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'when': 'W0',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'verbose',
        },
       
        'user-logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/user.log'),
            'when': 'W0',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'verbose',
        },

        'download-logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/download.log'),
            'when': 'W0',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'disabled': False
        },
        '': {
            'handlers': ['console', 'app-logfile'],
            'level': 'DEBUG',
            'disabled': False
        },
        'project_app': {
            'handlers': ['console', 'app-logfile'],
            'level': 'DEBUG',
            'disabled': False,
            'propagate': False
        },
        'project_user': {
            'handlers': ['console', 'user-logfile'],
            'level': 'DEBUG',
            'disabled': False,
            'propagate': False
        },
        'download_user': {
            'handlers': ['console', 'download-logfile'],
            'level': 'DEBUG',
            'disabled': False,
            'propagate': False
        },
    },
}


