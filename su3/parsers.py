from functools import partial
import logging
import os

from pion.parsing.lec import PionLECParser
from su3.models import PionLECSU3


log = logging.getLogger(__name__)


def parse_lecs_from_folder(folder):
    all_data = PionLECParser().get_from_folder(folder)
    bulk_list = [PionLECSU3(**d) for d in all_data]
    PionLECSU3.objects.insert(bulk_list)

lec_24c = partial(parse_lecs_from_folder, os.path.join('data', '24c', 'lec',
                                                       'pion_lecs', 'su3'))

parsers = [
    {
        'name': '24c SU3 Pion LECS',
        'parser': lec_24c,
    }
]
