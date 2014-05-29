# Create your views here.
from collections import defaultdict
import logging
from pprint import pprint
from pyon.lib.meson import PseudoscalarChargedMeson
from meas24c.models import ChargedMeson24c
from delmsq.lib.statistics import equivalent_params
import numpy as np

ps_mesons_005 = ChargedMeson24c.objects(m_l=0.005, source='GFWALL',
                                        sink='GAM_5')
ps_mesons_01 = ChargedMeson24c.objects(m_l=0.01, source='GFWALL', sink='GAM_5')
ps_mesons_02 = ChargedMeson24c.objects(m_l=0.02, source='GFWALL', sink='GAM_5')
ps_mesons_03 = ChargedMeson24c.objects(m_l=0.03, source='GFWALL', sink='GAM_5')


def get_charged_mesons(mesons):
    """
    Rewritten for `mongoengine`
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
        all_mesons[(m1, m2, q1, q2)] = [{'config_number': cn, 'data': data}
                                        for cn, data in
                                        zip(conf_numbers, all_data)]
    logging.debug("Creating objects")
    for m1, m2, q1, q2 in list(all_mesons):
        logging.debug("Adding {} {}".format((m1, m2), (q1, q2)))
        if (m1, m2, q1, q2) in already_done:
            continue
        fd = []  # filtered_data
        conf_numbers = None
        for mm1, mm2, qq1, qq2 in equivalent_params(m1, m2, q1, q2):
            try:
                one_mass = all_mesons[(mm1, mm2, qq1, qq2)]
            except KeyError:
                continue
            already_done.add((mm1, mm2, qq1, qq2))
            if len(one_mass) == 0:
                continue
            fd.append([q['data'] for q in one_mass])
            conf_numbers = [q['config_number'] for q in one_mass]
        if not conf_numbers:
            raise ValueError("No matches")
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


def get_uncharged_mesons(mesons):
    uncharged_hadrons = {}
    already_done = set()
    uncharged = mesons(charge_1=0, charge_2=0).exclude("m_l")

    for meson in uncharged:
        m1 = meson.mass_1
        m2 = meson.mass_2
        if (m1, m2) in already_done:
            continue
        #one_mass = uncharged(mass_1=m1, mass_2=m2)

        already_done.add((m1, m2))
        logging.debug("Adding {}".format((m1, m2)))
        # fd = [[s.re for s in q.data] for q in one_mass]
        # config_numbers = [q.config_number for q in one_mass]
        config_numbers = [c.config_number for c in meson.correlators]
        fd = [[s.re for s in c.data] for c in meson.correlators]
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

