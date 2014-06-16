from functools import partial
import logging
import os

from pion.parsing.lec import parse_lecs_from_folder


log = logging.getLogger(__name__)

lec_24c = partial(parse_lecs_from_folder, os.path.join('data', '24c', 'lec',
                                                       'pion_lecs'))

parsers = [
    {
        'name': '24c Pion LECS',
        'parser': lec_24c,
    }
]
