from functools import partial
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qed.settings")
from meas24c.parsing.correlators import parse_correlators_from_folder
import logging
log = logging.getLogger(__name__)

root_folder = os.path.join('data', '24c', 'correlators')


def make_parser(folder, m_l):
    return partial(parse_correlators_from_folder, folder, m_l)

parsers = [
    {
        'name': '0.02',
        'parser': make_parser(os.path.join(root_folder, '0.02'), 0.02)
    },
    {
        'name': '0.005',
        'parser': make_parser(os.path.join(root_folder, '0.005'), 0.005)
    },
    {
        'name': '0.03',
        'parser': make_parser(os.path.join(root_folder, '0.03'), 0.03)
    },
    {
        'name': '0.01, 0.005',
        'parser': make_parser(os.path.join(root_folder, 'mv0.001-msea0.005'),
                              0.005)
    },
    {
        'name': '0.01, 0.01',
        'parser': make_parser(os.path.join(root_folder, 'mv0.001-msea0.01'),
                              0.01)
    },
    {
        'name': '0.01',
        'parser': make_parser(os.path.join(root_folder, '0.01-1-180'),
                              0.01)
    },
]
