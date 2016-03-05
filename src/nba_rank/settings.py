import os

from django.contrib.messages import constants as messages
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.dirname(BASE_DIR)

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(DATA_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'nba_rank', 'static'),
]

LOCALE_PATHS = [os.path.join(DATA_DIR, 'locale')]

ROOT_URLCONF = 'nba_rank.urls'
WSGI_APPLICATION = 'nba_rank.wsgi.application'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # nba_rank
    'players',
    'misc',

    # other
    'kronos',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
             os.path.join(BASE_DIR, 'nba_rank', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'players.context_processors.seasons',
            ],
        },
    },
]


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/Warsaw'
USE_I18N = True
USE_L10N = True
USE_TZ = True


################
# Own settings #
################

# For Django messages and Bootstrap 3 compatibility
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# Local settings
try:
    from .local_settings import *
except ImportError:
    pass
