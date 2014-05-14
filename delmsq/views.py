"""
A :func:`view` is a particular aspect of a :class:`Model`

A view is used as a way to separate data from formulae. The return value of a
view function should be whatever data that a formulae uses.
"""
from pyon.lib.meson import PseudoscalarChargedMeson
from delmsq.models import ChargedMeson
import logging
from delmsq.lib.statistics import equivalent_params
import numpy as np

# pseudoscalar mesons
ps_mesons = ChargedMeson.objects.filter(source='GAM_5', sink='GAM_5')


def charged_mesons():
    charged_hadrons = {}
    charged = ps_mesons.exclude(charge_1=0, charge_2=0)
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
            one_mass = charged.filter(mass_1=mm1, mass_2=mm2,
                                      charge_1=qq1, charge_2=qq2)
            already_done.add((mm1, mm2, qq1, qq2))
            # TODO aggregrate to do average?
            fd.append([[s.re for s in q.data.all()] for q in one_mass])
        average_data = np.average(fd, axis=0)
        config_numbers = [q.config_number for q in one_mass]
        had = PseudoscalarChargedMeson(
            average_data,
            masses=(m1, m2),
            charges=(q1, q2),
            config_numbers=config_numbers
        )
        had.sort()
        had.fold()
        had.scale()
        charged_hadrons[(m1, m2, q1, q2)] = had
    return charged_hadrons


def uncharged_mesons():
    uncharged_hadrons = {}
    already_done = set()
    uncharged = ps_mesons.filter(charge_1=0, charge_2=0)
    # TODO use F statements to speed it up?

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
        had = PseudoscalarChargedMeson(
            fd,
            masses=(m1, m2),
            charges=(0, 0),
            config_numbers=config_numbers
        )
        had.sort()
        had.fold()
        had.scale()
        uncharged_hadrons[(m1, m2)] = had
    return uncharged_hadrons

