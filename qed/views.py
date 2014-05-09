# from collections import defaultdict
# import copy
# import logging
# import itertools
# # from pyon.runner.query import QuerySet
# import numpy as np
# # from qed.sources import MesonDBSource, MesonSource
#
# __author__ = 'srd1g10'
# """
# A view is a queryset (some aspect of data) combined with a model.
# """
# from qed.lib.statistics import equivalent_params
#
# # pseudo_src = MesonDBSource()
# #pseudo_src = MesonSource()
# pseudoscalar_mesons = pseudo_src.filter(source='GAM_5', sink='GAM_5')
#
#
# def charged_mesons():
#     logging.debug("Charged")
#     vu = pseudo_src
#     masses = vu.unique('masses')
#     charges = vu.unique('charges')
#     charges = [c for c in charges if c != (0, 0)]
#     config_numbers = sorted(vu.unique('config_number'))
#     combinations = itertools.product(masses, charges)
#     filtered_data = defaultdict(list)
#     manager_class = vu.manager_class
#     already_done = set()
#
#     for comb in combinations:
#         if comb in already_done:
#             continue
#         logging.debug("Adding {}".format(comb))
#         for cn in config_numbers:
#             fd = []
#             central_params = None
#             for m, q in equivalent_params(
#                     *list(itertools.chain.from_iterable(comb))):
#                 # average over equivalent masses
#                 matched = vu.filter(config_number=cn, masses=m,
#                                     charges=q, source='GAM_5',
#                                     sink='GAM_5').results
#                 if len(matched) > 1:
#                     raise ValueError(
#                         "Could not get a unique match for {} {} {}"
#                         .format(cn, m, q))
#
#                 dat = copy.deepcopy(matched[0])
#                 fd.append(dat['data'])
#                 central_params = dat
#                 already_done.add((m, q))
#             averaged_data = np.average(fd, axis=0)
#             central_params['data'] = averaged_data
#             filtered_data[comb].append(central_params)
#         filtered_data[comb] = QuerySet(filtered_data[comb], manager_class)
#
#     return filtered_data
#
#
# #@app.register_view('uncharged')
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
