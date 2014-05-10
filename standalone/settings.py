import logging
import os

APP_NAME = 'delta_m_squared'
PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
APP_FOLDER = os.path.join(PROJECT_ROOT, '')
DUMP_DIR = os.path.join(PROJECT_ROOT, '../results')
LOGGING_LEVEL = logging.DEBUG

# Django things
SECRET_KEY = 'foo'
INSTALLED_APPS = ("qed", )
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'qed.db',
    }
}
