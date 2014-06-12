import logging
log = logging.getLogger(__name__)



parsers = [
    {
        'name': 'Meas24c Correlators',
        'parser': 'meas24c.parsers',
    },
#     {
#         'name': 'Kaon LECs',
#         'parser': 'kaon.parsers',
#     }
]