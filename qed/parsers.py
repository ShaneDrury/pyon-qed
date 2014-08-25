import logging
log = logging.getLogger(__name__)


parsers = [
    {
        'name': '24c Correlators',
        'parser': 'meas24c.parsers',
        'enabled': False,
    },

    {
        'name': 'SU3 Pion LECs',
        'parser': 'su3.parsers',
        'enabled': False,
    },

    {
        'name': 'SU2 Pion LECs',
        'parser': 'su2.parsers',
        'enabled': False,
    },
]