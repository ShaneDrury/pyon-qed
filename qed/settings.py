import logging
import os


PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
DUMP_DIR = os.path.join(PROJECT_ROOT, '../results')
LOGGING_LEVEL = logging.DEBUG
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, '../templates'),
)
ROOT_MEASUREMENTS = 'qed.measurements'

# Django things
SECRET_KEY = 'foo'
INSTALLED_APPS = (
    'qed',
    'delmsq',
    'meas2'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'qed.db',
    }
}
