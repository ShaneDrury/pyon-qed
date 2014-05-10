"""
A view is a particular aspect of some data e.g. a filtered QuerySet
"""
from pyon.lib.meson import PseudoscalarChargedMeson
from qed.models import Iwasaki32cChargedMeson
from collections import defaultdict
import copy
import itertools
import logging
from qed.lib.statistics import equivalent_params
import numpy as np
# pseudoscalar mesons
ps_mesons = Iwasaki32cChargedMeson.objects.filter(source='GAM_5', sink='GAM_5')


def charged_mesons():
    logging.debug("Charged")
    qs = ps_mesons

    masses = qs.values_list('mass_1', flat=True).distinct()
    charges = qs.values_list('charge_1', flat=True).distinct()

    charges = [c for c in charges if c != (0, 0)]  # charged
    config_numbers = sorted(
        qs.values_list('config_number', flat=True).distinct()
    )
    combinations = itertools.product(masses, masses, charges, charges)
    filtered_data = {}
    already_done = set()

    for comb in combinations:
        if comb in already_done:
            continue
        logging.debug("Adding {}".format(comb))
        averaged_data = []
        for cn in config_numbers:
            fd = []
            central_params = None
            for m1, m2, q1, q2 in equivalent_params(*comb):
                # average over equivalent masses
                dat = qs.get(config_number=cn, mass_1=m1, mass_2=m2,
                             charge_1=q1, charge_2=q2,
                             source='GAM_5', sink='GAM_5')
                fd.append([s.re for s in dat.data.all()])
                central_params = dat
                already_done.add((m1, m2, q1, q2))
            averaged_data.append(np.average(fd, axis=0))
        masses = (central_params.mass_1, central_params.mass_2)
        charges = (central_params.charge_1, central_params.charge_2)
        filtered_data[comb] = PseudoscalarChargedMeson(averaged_data,
                                                       masses=masses,
                                                       charges=charges,
                                                       config_numbers=config_numbers)
    return filtered_data


def uncharged_mesons():
    logging.debug("Uncharged")
    qs = ps_mesons

    masses = qs.values_list('mass_1', flat=True).distinct()
    filtered_data = {}
    already_done = set()
    for m1, m2 in itertools.product(masses, masses):
        if (m1, m2) in already_done:
            continue
        already_done.add((m1, m2))
        logging.debug("Adding {}".format((m1, m2)))
        dat = qs.filter(mass_1=m1, mass_2=m2, charge_1=0, charge_2=0)
        fd = [[s.re for s in q.data.all()] for q in dat.all()]
        config_numbers = [q.config_number for q in dat.all()]
        filtered_data[(m1, m2)] = PseudoscalarChargedMeson(fd,
                                                           masses=masses,
                                                           charges=(0, 0),
                                                           config_numbers=config_numbers)
    return filtered_data


# def uncharged_mesons():
#     vu = pseudo_src
#     masses = vu.unique('masses')
#     already_done = set()
#     filtered_data = {}
#     for m in masses:
#         if m in already_done:
#             continue
#         logging.debug("Adding {}".format(m))
#         already_done.add(m)
#         dat = vu.filter(masses=m, charges=(0, 0))
#         filtered_data[m] = dat
#     return filtered_data
#
#
# #@app.register_view('all_mesons')
# def all_mesons():
#     return {'charged_mesons': charged_mesons(),
#             'uncharged_mesons': uncharged_mesons()}
#
