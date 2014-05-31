from functools import partial

import numpy as np
from pyon.core.cache import cache_data

from delmsq.lib.fitting import MinuitFitter, all_del_m_sq
from meas24c.views import get_charged_mesons, get_uncharged_mesons
from meas24c.views import ps_mesons_005, ps_mesons_01, ps_mesons_02, \
    ps_mesons_03


bnds = ((0., 1.), (0, None))
fit_params_uncovariant = dict(fit_range=np.array(range(9, 32+1)),
                              initial_value=dict(m=0.18, c=1.39432),
                              covariant=False,
                              bounds=bnds)

fit_params_covariant = fit_params_uncovariant.copy()
fit_params_covariant['covariant'] = True
fit_params_correlated = fit_params_covariant.copy()
fit_params_correlated['correlated'] = True

#  TODO: Maybe make this into a loop


@cache_data()
def charged_005():
    return partial(get_charged_mesons, mesons=ps_mesons_005)


@cache_data()
def uncharged_005():
    return partial(get_uncharged_mesons, mesons=ps_mesons_005)


@cache_data()
def charged_01():
    return partial(get_charged_mesons, mesons=ps_mesons_01)


@cache_data()
def uncharged_01():
    return partial(get_uncharged_mesons, mesons=ps_mesons_01)


@cache_data()
def charged_02():
    return partial(get_charged_mesons, mesons=ps_mesons_02)


@cache_data()
def uncharged_02():
    return partial(get_uncharged_mesons, mesons=ps_mesons_02)


@cache_data()
def charged_03():
    return partial(get_charged_mesons, mesons=ps_mesons_03)


@cache_data()
def uncharged_03():
    return partial(get_uncharged_mesons, mesons=ps_mesons_03)

uncovariant_func = partial(all_del_m_sq,
                           hadron1_kwargs=fit_params_uncovariant,
                           hadron2_kwargs=fit_params_uncovariant,
                           method=MinuitFitter)

covariant_func = partial(all_del_m_sq,
                         hadron1_kwargs=fit_params_covariant,
                         hadron2_kwargs=fit_params_covariant,
                         method=MinuitFitter)

uncovariant_005 = partial(uncovariant_func,
                          uncharged_hadrons=uncharged_005,
                          charged_hadrons=charged_005)

uncovariant_01 = partial(uncovariant_func,
                         uncharged_hadrons=uncharged_01,
                         charged_hadrons=charged_01)

uncovariant_02 = partial(uncovariant_func,
                         uncharged_hadrons=uncharged_02,
                         charged_hadrons=charged_02)

uncovariant_03 = partial(uncovariant_func,
                         uncharged_hadrons=uncharged_03,
                         charged_hadrons=charged_03)

covariant_005 = partial(covariant_func,
                        uncharged_hadrons=uncharged_005,
                        charged_hadrons=charged_005)

covariant_01 = partial(covariant_func,
                       uncharged_hadrons=uncharged_01,
                       charged_hadrons=charged_01)

covariant_02 = partial(covariant_func,
                       uncharged_hadrons=uncharged_02,
                       charged_hadrons=charged_02)

covariant_03 = partial(covariant_func,
                       uncharged_hadrons=uncharged_03,
                       charged_hadrons=charged_03)

measurements = [
    # {
    #     'name': 'ml_0.005_cov', 'measurement': covariant_005,
    #     'template_name' : 'delmsq/index.html'
    # },
    # {
    #     'name': 'ml_0.01_cov', 'measurement': covariant_01,
    #     'template_name' : 'delmsq/index.html'
    # },
    # {
    #     'name': 'ml_0.02_cov', 'measurement': covariant_02,
    #     'template_name' : 'delmsq/index.html'
    # },
    # {
    #     'name': 'ml_0.03_cov', 'measurement': covariant_03,
    #     'template_name' : 'delmsq/index.html'
    # },
    {
        'name': 'ml_0.005_uncov', 'measurement': uncovariant_005,
        'template_name' : 'delmsq/index.html'
    },
    {
        'name': 'ml_0.01_uncov', 'measurement': uncovariant_01,
        'template_name' : 'delmsq/index.html'
    },
    {
        'name': 'ml_0.02_uncov', 'measurement': uncovariant_02,
        'template_name' : 'delmsq/index.html'
    },
    {
        'name': 'ml_0.03_uncov', 'measurement': uncovariant_03,
        'template_name' : 'delmsq/index.html'
    },
    ]