# Create your views here.
from collections import defaultdict
import logging
from django.utils import six
from pyon.lib.meson import PseudoscalarChargedMeson
from meas24c.models import ChargedMeson24c, TimeSlice
from delmsq.lib.statistics import equivalent_params
import numpy as np

ps_mesons_005 = ChargedMeson24c.objects.filter(source='GFWALL', sink='GAM_5',
                                               m_l=0.005)

ps_mesons_01 = ChargedMeson24c.objects.filter(source='GFWALL', sink='GAM_5',
                                              m_l=0.01)

ps_mesons_02 = ChargedMeson24c.objects.filter(source='GFWALL', sink='GAM_5',
                                              m_l=0.02)

ps_mesons_03 = ChargedMeson24c.objects.filter(source='GFWALL', sink='GAM_5',
                                              m_l=0.03)


def get_charged_mesons(mesons):
    """
    A new approach. Get all the data we will need at once and use python
    to filter this. This should avoid multiple round-trips.
    """
    charged_hadrons = {}
    already_done = set()
    charged = mesons.exclude(charge_1=0, charge_2=0).iterator()

    all_mesons = defaultdict(list)
    for meson in charged:  # save all the data in a dict
        m1 = meson.mass_1
        m2 = meson.mass_2
        q1 = meson.charge_1
        q2 = meson.charge_2
        cn = meson.config_number
        # logging.debug("Adding {} {} {}".format((m1, m2), (q1, q2), cn))
        if (m1, m2, q1, q2, cn) in all_mesons:
            raise ValueError
        all_mesons[(m1, m2, q1, q2)].append({'config_number': cn,
                                             'data': [s.re for s in meson.data.all()]})
    for m1, m2, q1, q2 in list(all_mesons):
        if (m1, m2, q1, q2) in already_done:
            continue
        fd = []  # filtered_data
        for mm1, mm2, qq1, qq2 in equivalent_params(m1, m2, q1, q2):
            one_mass = all_mesons[(mm1, mm2, qq1, qq2)]
            already_done.add((mm1, mm2, qq1, qq2))
            if len(one_mass) == 0:
                continue
            fd.append([q['data'] for q in one_mass])
            conf_numbers = [q['config_number'] for q in one_mass]
        average_data = np.average(fd, axis=0)
        had = PseudoscalarChargedMeson(
            average_data,
            masses=(m1, m2),
            charges=(q1, q2),
            config_numbers=conf_numbers
        )
        had.sort()
        had.fold()
        had.scale()
        charged_hadrons[(m1, m2, q1, q2)] = had
    return charged_hadrons

# SLOWER
# def get_charged_mesons(m_l):
#     """
#     Reverse the lookup. Select from timeslices where the related meson has the
#     properties that we want.
#     """
#     charged_hadrons = {}
#     already_done = set()
#     light_masses = TimeSlice.objects.filter(meson__m_l=m_l,
#                                             meson__source='GFWALL',
#                                             meson__sink='GAM_5',
#                                             ).exclude(
#                                                 meson__charge_1=0,
#                                                 meson__charge_2=0
#                                             )
#     combs = light_masses.values_list('meson__mass_1', 'meson__mass_2',
#                                      'meson__charge_1', 'meson__charge_2'
#                                      ).distinct()
#
#     for c in combs:
#         logging.debug(c)
#         if c in already_done:
#             continue
#         fd = []
#         for equiv in equivalent_params(*c):
#             m_1, m_2, q_1, q_2 = equiv
#             qs = light_masses.filter(meson__mass_1=m_1, meson__mass_2=m_2,
#                                      meson__charge_1=q_1, meson__charge_2=q_2)
#             if not qs.exists():
#                 continue
#             already_done.add((m_1, m_2, q_1, q_2))
#             fd.append([q.re for q in qs])
#
#         average_data = np.average(fd, axis=0)
#         config_numbers = [q.config_number for q in qs]
#         # had = PseudoscalarChargedMeson(
#         #     average_data,
#         #     masses=(m1, m2),
#         #     charges=(q1, q2),
#         #     config_numbers=config_numbers
#         # )
#         # had.sort()
#         # had.fold()
#         # had.scale()
#         # charged_hadrons[(m1, m2, q1, q2)] = had
