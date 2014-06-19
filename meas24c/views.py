# Create your views here.
import logging

from mongoengine import Q
import numpy as np

from delmsq.lib.statistics import equivalent_params


log = logging.getLogger(__name__)


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
    qs = mesons(Q(charge_1__ne=0) or Q(charge_2__ne=0)).exclude("m_l")
    # Q(charge_1=0) or Q(charge_2=0)
    all_mesons = {}
    log.debug("Getting all data")
    for meson in qs:
        m1 = meson.mass_1
        m2 = meson.mass_2
        q1 = meson.charge_1
        q2 = meson.charge_2
        correlators = meson.correlators
        conf_numbers = [c.config_number for c in correlators]
        all_data = [[s.re for s in c.data] for c in correlators]
        log.debug("Adding {} {}".format((m1, m2), (q1, q2)))
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

        charged_hadrons[(m1, m2, q1, q2)] = {'data': average_data,
                                             'config_numbers': all_conf_numbers[0]}
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
        log.debug("Adding {}".format((m1, m2)))
        uncharged_hadrons[(m1, m2, 0, 0)] = {'data': all_data,
                                             'config_numbers': conf_numbers}
    return uncharged_hadrons

