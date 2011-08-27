# -*- coding: utf-8 -*-
import os

PROJECT_ROOT = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static', 'gamesoup'),
)

# Login paths
LOGIN_REDIRECT_URL = '/admin/'

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'gamesoup.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
)

TEST_RUNNER = 'alphacabbage.django.test.run_tests'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'django.contrib.sites',

    'debug_toolbar',
    
    'alphacabbage.django.helpers',
    'alphacabbage.django.graphs',
    'alphacabbage.django.tracer',

    'gamesoup.expressions',
    'gamesoup.library',
    'gamesoup.games',
    'gamesoup.matches',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

try:
    from local_settings import *
except ImportError:
    pass
