# -*- coding: utf-8 -*-
#
# This is a sample local settings configuration file. To get your Django
# environment setup, you need to create a localsettings.py file. From the
# command line,
#
#   cp localsettings_example.py localsettings.py
#
# and then edit the contents of that file where-ever you see a:
#
#   # <= Customize
#
import os

PROJECT_ROOT = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = '!1t8ENM]~1c\ik,aD7@nidrj{da[zc9]\wSG@6wo~E(rj.XIs?'

#django-contact-form
DEFAULT_FROM_EMAIL = 'contactform@foo'

MANAGERS = (
    ('Kevin Tonon','kevin@betweenconcepts.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'development.sqlite'),
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ABC'
EMAIL_HOST_PASSWORD = 'ABC'
EMAIL_USE_TLS = True

CACHE_BACKEND = 'locmem:///'
CACHE_MIDDLEWARE_SECONDS = 60*5
CACHE_MIDDLEWARE_KEY_PREFIX = 'mingus.'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

INTERNAL_IPS = ('127.0.0.1',)

### DEBUG-TOOLBAR SETTINGS
DEBUG_TOOLBAR_CONFIG = {
'INTERCEPT_REDIRECTS': False,
}

#django-degug-toolbar
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

# Used by the library app as a scratch space for zipping and unzipping
# Type.code data in the bulk upload/download views.
LOCAL_EDITING_WORKSPACE = '%s/local-editing-workspace' % PROJECT_ROOT
