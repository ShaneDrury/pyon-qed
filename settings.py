import os

APP_NAME = 'delta_m_squared'
PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
APP_FOLDER = os.path.join(PROJECT_ROOT, 'qed')
DB_PATH = os.path.join(PROJECT_ROOT, 'qed.db')
#DB_USERNAME = 'srd1g10'
DUMP_DIR = os.path.join(PROJECT_ROOT, 'results')