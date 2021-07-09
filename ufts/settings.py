"""
Django settings for ufts ufts.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

from celery.schedules import crontab
from logging.handlers import SysLogHandler
from socket import gethostname, gethostbyname
from datetime import time
import logging
import os, sys


# from termsandconditions.decorators import terms_required

# Build paths inside the ufts like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTERNAL_LIBS_PATH = os.path.join(BASE_DIR, "ext_libs")
sys.path = ["", EXTERNAL_LIBS_PATH] + sys.path
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n9ucrt9=)e!d=(uaimum@7onn%uvua6a(m^9-=zmscd$&f%(%u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['ufts.lab', '172.16.16.205', '172.16.16.114', '127.0.0.1', 'localhost']
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
    'misc.apps.MiscConfig',
    'home.apps.HomeConfig',
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
    'django_ssl_auth.SSLClientAuthMiddleware',
    'django_admin_ip_restrictor.middleware.AdminIPRestrictorMiddleware',
    'lib.user_profile.check_userprofile_middleware',
]

AUTHENTICATION_BACKENDS = [
    'django_ssl_auth.SSLClientAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

RESTRICT_ADMIN=True
ALLOWED_ADMIN_IPS=['127.0.0.1', '::1', '192.168.1.1']
ALLOWED_ADMIN_IP_RANGES=['127.0.0.0/24', '::/1', '172.20.0.0/16', '172.16.16.0/24']
RESTRICTED_APP_NAMES=['admin']
TRUST_PRIVATE_IP=False

USER_DATA_FN = 'django_ssl_auth.cert.user_dict_from_dn'
AUTOCREATE_VALID_SSL_USERS = True


REQUEST_VALID_METHOD_NAMES = ('get', 'post', 'put', 'delete')
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
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}
# else:
DATABASES = {
 'default': {
     'ENGINE': 'django.db.backends.postgresql_psycopg2',
     'NAME': 'ufts',
     'USER': 'uftsuser',
     'PASSWORD': 'S3cr3tPWforUFTS',
     'HOST': 'db',
     'PORT': '5432',
 }
}

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
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_ROOT = '/opt/services/ufts/static/'
COMPRESS_PRECOMPILERS = (('text/x-scss', 'django_libsass.SassCompiler'),)

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_ROOT = '/opt/services/ufts/media/'
MEDIA_URL = '/media/'

SOFTWARE_ROOT = '/opt/services/ufts/software/'
SOFTWARE_URL = '/software/'

## 16GB File will be loaded in memory with this setting
## Only use if experiencing poor disk performance
# FILE_UPLOAD_MAX_MEMORY_SIZE = 1024*1024*1024*16

LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

CLASSIFICATION_TEXT = 'Unclassified'
CLASSIFICATION_TEXT_SHORT = '(U)'
CLASSIFICATION_TEXT_COLOR = 'black'
CLASSIFICATION_BACKGROUND_COLOR = 'green'
# CLASSIFICATION_LINK = '/security'

PRODUCT_NAME = 'UFTS'
OWNER = 'Juniper Networks'
VERSION = "1.0"
LICENSE_KEY = 'CBXS-V9K7-9CRR-PLU6-1LN4'
ACCESS_CODE = '1863'
COMPANY_NAME = 'Juniper Networks'
COMPANY_ADDRESS = '2251 Corporate Park Dr #100, Herndon, VA 20171'
COMPANY_PHONE = '(571) 203-1700'
THUMB_SIZE = (400, 400)
AUTH_USER_MODEL = 'users.CustomUser'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
IPWARE_META_PRECEDENCE_ORDER = (
     'REMOTE_ADDR',
     'HTTP_X_FORWARDED_FOR', 'X_FORWARDED_FOR',  # <client>, <proxy1>, <proxy2>
     'HTTP_CLIENT_IP',
     'HTTP_X_REAL_IP',
     'HTTP_X_FORWARDED',
     'HTTP_X_CLUSTER_CLIENT_IP',
     'HTTP_FORWARDED_FOR',
     'HTTP_FORWARDED',
     'HTTP_VIA',
 )
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
            'atTime': time(0,0,0),
            'formatter': 'verbose',
        },
        'upload-logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/upload.log'),
            'when': 'W0',
            'interval': 1,
            'backupCount': 7,
            'atTime': time(0,0,0),
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
        'upload_user': {
            'handlers': ['console', 'upload-logfile'],
            'level': 'DEBUG',
            'disabled': False,
            'propagate': False
        },
    },
}

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
# EMAIL_HOST = '192.168.2.5'
# EMAIL_PORT = 25
# # EMAIL_HOST_USER = 'testsite_app'
# # EMAIL_HOST_PASSWORD = 'mys3cr3tp4ssw0rd'
EMAIL_USE_TLS = False
FROM_EMAIL = 'ufts_noreply@example.com'
DEFAULT_FROM_EMAIL = FROM_EMAIL
REPORT_FORMAT = 'xlsx' #supported formats are pdf,xlsx, and docx

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    'daily_email': {
        'task': 'home.tasks.daily_email',
        'schedule': crontab(hour=23, minute=59)
    },
    'weekly_report': {
        'task': 'home.tasks.weekly_report_email',
        'schedule': crontab(day_of_week=0,hour=23,minute=59)
    },
}
