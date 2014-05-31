# Create your views here.
from collections import defaultdict
import logging
from pprint import pprint
from django.utils import six
from pyon.lib.meson import PseudoscalarChargedMeson
from meas24c.models import ChargedMeson24c, TimeSlice
from delmsq.lib.statistics import equivalent_params
import numpy as np

ps_mesons = ChargedMeson24c.objects.filter(source='GFWALL', sink='GAM_5')
ps_mesons_005 = ps_mesons(m_l=0.005)
ps_mesons_01 = ps_mesons(m_l=0.01)
ps_mesons_02 = ps_mesons(m_l=0.02)
ps_mesons_03 = ps_mesons(m_l=0.03)


def all_el_equal(lst):
    """
    Returns True if all elements in a list are equal to each other.
    """
    return lst[1:] == lst[:-1]

def get_charged_mesons(mesons):
    """
    A new approach. Get all the data we will need at once and use python
    to filter this. This should avoid multiple round-trips.
    """
    charged_hadrons = {}
    already_done = set()
    qs = mesons(charge_1__ne=0, charge_2__ne=0).exclude("m_l")
    all_mesons = {}
    logging.debug("Getting all data")
    for meson in qs:
        m1 = meson.mass_1
        m2 = meson.mass_2
        q1 = meson.charge_1
        q2 = meson.charge_2
        correlators = meson.correlators
        conf_numbers = [c.config_number for c in correlators]
        all_data = [[s.re for s in c.data] for c in correlators]
        logging.debug("Adding {} {}".format((m1, m2), (q1, q2)))
        if (m1, m2, q1, q2) in all_mesons:
            raise ValueError
        all_mesons[(m1, m2, q1, q2)] = {'config_numbers': conf_numbers,
                                        'data': all_data}
    for m1, m2, q1, q2 in list(all_mesons):
        if (m1, m2, q1, q2) in already_done:
            continue
        fd = []  # filtered_data
        all_conf_numbers = []
        for mm1, mm2, qq1, qq2 in equivalent_params(m1, m2, q1, q2):
            try:
                one_mass = all_mesons[(mm1, mm2, qq1, qq2)]
            except KeyError:
                continue
            already_done.add((mm1, mm2, qq1, qq2))
            if len(one_mass) == 0:
                continue
            fd.append(one_mass['data'])
            all_conf_numbers.append(one_mass['config_numbers'])

        if not all_el_equal(all_conf_numbers):
            raise ValueError("Averaging over non-identical "
                             "configuration numbers")
        average_data = np.average(fd, axis=0)
        had = PseudoscalarChargedMeson(
            average_data,
            masses=(m1, m2),
            charges=(q1, q2),
            config_numbers=all_conf_numbers[0]
        )
        had.sort()
        had.fold()
        had.scale()
        charged_hadrons[(m1, m2, q1, q2)] = had
    return charged_hadrons


def get_uncharged_mesons(mesons):
    uncharged_hadrons = {}
    already_done = set()
    uncharged = mesons(charge_1=0, charge_2=0).exclude("m_l")

    for meson in uncharged:
        m1 = meson.mass_1
        m2 = meson.mass_2
        if (m1, m2) in already_done:
            continue

        already_done.add((m1, m2))
        correlators = meson.correlators
        conf_numbers = [c.config_number for c in correlators]
        all_data = [[s.re for s in c.data] for c in correlators]
        logging.debug("Adding {}".format((m1, m2)))
        had = PseudoscalarChargedMeson(
            all_data,
            masses=(m1, m2),
            charges=(0, 0),
            config_numbers=conf_numbers
        )
        had.sort()
        had.fold()
        had.scale()
        uncharged_hadrons[(m1, m2)] = had
    return uncharged_hadrons

