import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qed.settings")
from meas24c.parsing.correlators import parse_correlators_from_folder
from meas24c.parsing.lec import parse_lecs_from_folder
import logging
log = logging.getLogger(__name__)

parsers = {}
def correlators():
    log.debug("Adding 0.02")
    parse_correlators_from_folder(os.path.join('data', '24c', 'correlators',
                                               '0.02'), 0.02)
    log.debug("Adding 0.005")
    parse_correlators_from_folder(os.path.join('data', '24c', 'correlators',
                                               '0.005'), 0.005)
    log.debug("Adding 0.03")
    parse_correlators_from_folder(os.path.join('data', '24c', 'correlators',
                                               '0.03'), 0.03)
    log.debug("Adding 0.001, 0.005")
    parse_correlators_from_folder(os.path.join('data', '24c', 'correlators',
                                               'mv0.001-msea0.005'), 0.005)
    log.debug("Adding 0.001, 0.01")
    parse_correlators_from_folder(os.path.join('data', '24c', 'correlators',
                                               'mv0.001-msea0.01'), 0.01)
    log.debug("Adding 0.01")
    parse_correlators_from_folder(os.path.join('data', '24c', 'correlators',
                                               '0.01-1-180'), 0.01)


def lecs():
    log.debug("Adding LECs")
    parse_lecs_from_folder(os.path.join('data', '24c', 'lec', 'pion_lecs'))
    log.debug("Done!")

if __name__ == '__main__':
    correlators()
    lecs()
