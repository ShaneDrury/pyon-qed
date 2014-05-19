import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qed.settings")
from django.conf import settings
from meas24c.parsing.correlators import parse_correlators_from_folder
from meas24c.parsing.lec import parse_lecs_from_folder
import logging
logging.basicConfig(level=settings.LOGGING_LEVEL)


def correlators():
    logging.debug("Adding 0.02")
    parse_correlators_from_folder(os.path.join('data', '24c', '0.02'), 0.02)
    logging.debug("Adding 0.005")
    parse_correlators_from_folder(os.path.join('data', '24c', '0.005'), 0.005)
    logging.debug("Adding 0.03")
    parse_correlators_from_folder(os.path.join('data', '24c', '0.03'), 0.03)
    logging.debug("Adding 0.001, 0.005")
    parse_correlators_from_folder(os.path.join('data', '24c', 'mv0.001-msea0.005'), 0.005)
    logging.debug("Adding 0.001, 0.01")
    parse_correlators_from_folder(os.path.join('data', '24c', 'mv0.001-msea0.01'), 0.01)
    logging.debug("Adding 0.01")
    parse_correlators_from_folder(os.path.join('data', '24c', '0.01-1-180'), 0.01)


def lecs():
    logging.debug("Adding LECs")
    parse_lecs_from_folder(os.path.join('data', '24c', 'lec', 'pion_lecs'))
    logging.debug("Done!")

if __name__ == '__main__':
    #correlators()
    lecs()
