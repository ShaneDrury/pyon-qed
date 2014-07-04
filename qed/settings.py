import logging
import os

import mongoengine


PROJECT_NAME = 'QED'
PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
DUMP_DIR = os.path.join(PROJECT_ROOT, '../results')
LOGGING_LEVEL = logging.DEBUG
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, '../templates'),
)
DEBUG = False
TEMPLATE_DEBUG = False
ROOT_MEASUREMENTS = 'qed.measurements'
ROOT_PARSERS = 'qed.parsers'

# Django things
SECRET_KEY = 'foo'
INSTALLED_APPS = (  # I don't think this does anything
    'qed',
    'delmsq',
    'meas24c',
    'pion',
    'kaon',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy'
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(PROJECT_ROOT, '../cache'),
    }
}


SESSION_ENGINE = 'mongoengine.django.sessions'  # optional
_MONGODB_USER = 'srd1g10'
_MONGODB_PASSWD = 'pass'
_MONGODB_HOST = 'localhost'
_MONGODB_NAME = 'qed'
_MONGODB_DATABASE_HOST = \
    'mongodb://%s:%s@%s/%s' \
    % (_MONGODB_USER, _MONGODB_PASSWD, _MONGODB_HOST, _MONGODB_NAME)

mongoengine.connect(_MONGODB_NAME, host=_MONGODB_DATABASE_HOST)
