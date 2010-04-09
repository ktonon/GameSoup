# Django settings for studyplay project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG
IS_LOCAL = False

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
SECRET_KEY = '-e4ab7m@6^8zmd!i@ih$@^t*bs#@us844hn)y10*b5m(4uyos$'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'gamesoup.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
)

TEST_RUNNER = 'alphacabbage.django.test.run_tests'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.markup',
    'django.contrib.sessions',
    'django.contrib.sites',

    'gamesoup.expressions',
    'gamesoup.library',
    'gamesoup.games',
    'gamesoup.matches',
    
    'alphacabbage.django.helpers',
    'alphacabbage.django.graphs',
    # 'studyplay.people',
    # 'gamesoup.library',
    # 'studyplay.play',

    # 'studyplay.boggle',

    # 'studyplay.choices',
    # 'studyplay.helpers',
    # 'studyplay.media',
    # 'studyplay.navigate',
)
