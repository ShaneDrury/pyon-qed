from functools import partial
import logging
import os

from kaon.parsers import KaonLECParser
from pion.parsing.lec import PionLECParser
from su2.models import PionLECSU2, KaonLECSU2


log = logging.getLogger(__name__)


def parse_pion_lecs_from_folder(folder):
    all_data = PionLECParser().get_from_folder(folder)
    bulk_list = [PionLECSU2(**d) for d in all_data]
    PionLECSU2.objects.insert(bulk_list)

get_24c_pion_lecs_su2 = partial(parse_pion_lecs_from_folder,
                                os.path.join('data', '24c', 'lec',
                                             'pion_lecs', 'su2'))


def parse_kaon_lecs_from_folder(folder, m_s):
    all_data = KaonLECParser().get_from_folder(folder)
    for d in all_data:
        d['m_s'] = m_s
    bulk_list = [KaonLECSU2(**d) for d in all_data]
    KaonLECSU2.objects.insert(bulk_list)

get_24c_kaon_lecs_su2_02 = partial(parse_kaon_lecs_from_folder,
                                   os.path.join('data', '24c', 'lec',
                                                'kaon_lecs', 'su2', '0.02'),
                                   0.02)

get_24c_kaon_lecs_su2_03 = partial(parse_kaon_lecs_from_folder,
                                   os.path.join('data', '24c', 'lec',
                                                'kaon_lecs', 'su2', '0.03'),
                                   0.03)

parsers = [
    {
        'name': '24c SU2 Pion LECS',
        'parser': get_24c_pion_lecs_su2,
        'enabled': False,
        },
    {
        'name': '24c SU2 Kaon LECS 0.02',
        'parser': get_24c_kaon_lecs_su2_02,
        },

    {
        'name': '24c SU2 Kaon LECS 0.03',
        'parser': get_24c_kaon_lecs_su2_03,
        },

    ]