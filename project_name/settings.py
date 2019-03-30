"""
Django settings for sqs_dispatcher project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import json
import os

import environ

root = environ.Path(__file__) - 3  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False), )  # set default values and casting
environ.Env.read_env()  # reading .env file

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = root()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DJANGO_DEBUG')

DEBUG_TOOLBAR_ENABLE = env('DJANGO_DEBUG_TOOLBAR_ENABLE')

ALLOWED_HOSTS = [
    '*',
]

INTERNAL_IPS = [
    '127.0.0.1',
    '192.168.1.108',
]

USE_I18N = env('DJANGO_USE_I18N')

USE_L10N = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'django_extensions',
    "compressor",
    'debug_toolbar' if DEBUG_TOOLBAR_ENABLE else None,
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
if DEBUG_TOOLBAR_ENABLE:
    MIDDLEWARE = MIDDLEWARE + [
        #  include the Debug Toolbar middleware as early as possible in the list. However, it must come after any other middleware that encodes the response’s content, such as GZipMiddleware.
        # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
        'debug_toolbar.middleware.DebugToolbarMiddleware',

    ]

if USE_I18N:
    MIDDLEWARE = [y
                  for i, x in enumerate(MIDDLEWARE)
                  for y in (('django.middleware.locale.LocaleMiddleware', x)
                            if MIDDLEWARE[i - 1] == 'django.contrib.sessions.middleware.SessionMiddleware'
                            else (x,))]

# https://django-debug-toolbar.readthedocs.org
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TEMPLATE_CONTEXT': True,
    'ENABLE_STACKTRACES': True,
    'SQL_WARNING_THRESHOLD': 100,  # milliseconds
    'JQUERY_URL': "https://cdn.bootcss.com/jquery/2.2.4/jquery.min.js",
    # only for super user
    # "SHOW_TOOLBAR_CALLBACK": lambda request: not request.is_ajax() and request.user and request.user.is_superuser
}
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

ROOT_URLCONF = '{{ project_name }}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'project_templates'),
        ],
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

WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

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
# When support for time zones is enabled, Django stores datetime information in UTC in the database, uses time-zone-aware datetime objects internally, and translates them to the end user’s time zone in templates and forms.
# This is handy if your users live in more than one time zone and you want to display datetime information according to each user’s wall clock.
# https://docs.djangoproject.com/en/2.1/topics/i18n/timezones/
USE_TZ = True

#  default time zone
# TIME_ZONE = 'Asia/Shanghai'
TIME_ZONE = 'UTC'

# it provides a fallback language
# LANGUAGE_CODE = 'zh-Hans'

from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ('en', _('English')),
    ('zh-cn', _('Chinese')),
    # ('zh', '简体中文'),
    # ('zh-cn', '简体中文'),
    # ('zh-tw', '繁體中文'),
    # ('de', _('German')),
)

public_root = root.path('public/')

# MEDIA_ROOT = public_root('media')
# MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
#  list of folders where Django will search for additional static files aside from the static folder of each app installed
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "project_static"),
    # '/var/www/static/',
)
# the folder where static files will be stored after using manage.py collectstatic
# STATIC_ROOT is useless during development, it's required by nginx,
# as Nginx doesn't know anything about your django project and doesn't know where to find static files.
#    location ^~ /static {
#           alias /project/path/www/;
#     }
STATIC_ROOT = public_root('static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',
)

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# SESSION_COOKIE_SECURE = False
# SECURE_BROWSER_XSS_FILTER = False
# SECURE_CONTENT_TYPE_NOSNIFF = False
# SECURE_HSTS_INCLUDE_SUBDOMAINS = False
# SECURE_HSTS_SECONDS = 86400
# SECURE_REDIRECT_EXEMPT = []
# SECURE_SSL_HOST = None
# SECURE_SSL_REDIRECT = False
# SECURE_PROXY_SSL_HEADER = (
#     ('HTTP_X_FORWARDED_PROTO', 'https'),
# )

# rest framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.authentication.BearerTokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}

# Sentry
SENTRY_DSN = env('SENTRY_DSN')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
    )

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': env.db(),  # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'extra': env.db('SQLITE_URL', default='sqlite:////tmp/my-tmp-sqlite.db')
}
