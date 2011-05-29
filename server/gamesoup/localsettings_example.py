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
from settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
IS_LOCAL = True

ADMINS = (
    ('Your Name', 'your@email.com'), # <= Customize
)
MANAGERS = ADMINS

# Replace '/path/to/' with the path to your gamesoup working copy.
PROJECT_ROOT = '/path/to/gamesoup/server' # <= Customize

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '%s/db/development.sqlite' % PROJECT_ROOT

MEDIA_ROOT = '%s/media/' % PROJECT_ROOT
MEDIA_URL = '/site-media/'
ADMIN_MEDIA_PREFIX = '/django-admin-media/'

# Used by the library app as a scratch space for zipping and unzipping
# Type.code data in the bulk upload/download views.
LOCAL_EDITING_WORKSPACE = '%s/local-editing-workspace' % PROJECT_ROOT

TEMPLATE_DIRS = (
    '%s/templates' % PROJECT_ROOT,
    '%s/../support/AlphaCabbage/alphacabbage/django/graphs/templates' % PROJECT_ROOT,
    )

FIXTURE_DIRS = (
    '%s/fixtures' % PROJECT_ROOT,
    )

# To determine ADMIN_MEDIA_ROOT
# From a command line:
#
#   python
#   >>> import django
#   >>> django
#   <module 'django' from '/usr/local/lib/python2.7/site-packages/django/__init__.pyc'>
#
# If that is what you saw, then you ADMIN_MEDIA_ROOT would be:
# 
#   '/usr/local/lib/python2.7/site-packages/django/contrib/admin/media/'
#
# I.e. Find the path to your django installation and replace the package file
# '__init__.pyc' with 'contrib/admin/media/'
ADMIN_MEDIA_ROOT = 'See instructions' # <= Customize
