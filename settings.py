import logging
import os


PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
DUMP_DIR = os.path.join(PROJECT_ROOT, 'results')
LOGGING_LEVEL = logging.DEBUG
MEASUREMENTS = ('delmsq.measurement.del_m_sq_0042', )

# Django things
SECRET_KEY = 'foo'
INSTALLED_APPS = ("delmsq", )
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'qed.db',
    }
}
