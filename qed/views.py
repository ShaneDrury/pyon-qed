"""
A view is a particular aspect of some data e.g. a filtered QuerySet
"""
from pyon.lib.meson import PseudoscalarChargedMeson
from qed.models import Iwasaki32cChargedMeson
import logging
from qed.lib.statistics import equivalent_params
import numpy as np

# pseudoscalar mesons
ps_mesons = Iwasaki32cChargedMeson.objects.filter(source='GAM_5', sink='GAM_5')


#@profile
def charged_mesons():
    logging.debug("Charged")

    filtered_data = {}
    qs = ps_mesons
    charged = qs.exclude(charge_1=0, charge_2=0)
    already_done = set()
    for meson in charged:
        m1 = meson.mass_1
        m2 = meson.mass_2
        q1 = meson.charge_1
        q2 = meson.charge_2
        if (m1, m2, q1, q2) in already_done:
            continue
        logging.debug("Adding {} {}".format((m1, m2), (q1, q2)))
        fd = []
        for mm1, mm2, qq1, qq2 in equivalent_params(m1, m2, q1, q2):
            one_mass = qs.filter(mass_1=mm1, mass_2=mm2,
                                 charge_1=qq1, charge_2=qq2)
            already_done.add((mm1, mm2, qq1, qq2))

            fd.append([[s.re for s in q.data.all()] for q in one_mass])
        average_data = np.average(fd, axis=0)
        config_numbers = [q.config_number for q in one_mass]
        filtered_data[(m1, m2, q1, q2)] = PseudoscalarChargedMeson(
            average_data,
            masses=(m1, m2),
            charges=(q1, q2),
            config_numbers=config_numbers
        )
    return filtered_data


def uncharged_mesons():
    logging.debug("Uncharged")
    qs = ps_mesons

    filtered_data = {}
    already_done = set()
    uncharged = qs.filter(charge_1=0, charge_2=0)
    for meson in uncharged:
        m1 = meson.mass_1
        m2 = meson.mass_2
        if (m1, m2) in already_done:
            continue
        one_mass = uncharged.filter(mass_1=m1, mass_2=m2)

        already_done.add((m1, m2))
        logging.debug("Adding {}".format((m1, m2)))

        fd = [[s.re for s in q.data.all()] for q in one_mass]
        config_numbers = [q.config_number for q in one_mass]
        filtered_data[(m1, m2)] = PseudoscalarChargedMeson(
            fd,
            masses=(m1, m2),
            charges=(0, 0),
            config_numbers=config_numbers
        )
    return filtered_data

