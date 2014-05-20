from functools import partial
import numpy as np
from pyon.runner.measurement import Measurement
from delmsq.lib.fitting import MinuitFitter, all_del_m_sq
from delmsq.views import get_charged_mesons, get_uncharged_mesons
from meas24c.views import ps_mesons_005, ps_mesons_01, ps_mesons_02, \
    ps_mesons_03


bnds = ((0., 1.), (0, None))
fit_params_uncovariant = dict(fit_range=np.array(range(9, 32+1)),
                              initial_value=dict(m=0.18, c=1.39432),
                              #initial_value=[0.18, 1.39432],
                              covariant=False,
                              bounds=bnds)

fit_params_covariant = fit_params_uncovariant
fit_params_covariant['covariant'] = True
fit_params_correlated = fit_params_covariant
fit_params_correlated['correlated'] = True

charged_005 = partial(get_charged_mesons, mesons=ps_mesons_005)
uncharged_005 = partial(get_uncharged_mesons, mesons=ps_mesons_005)

charged_01 = partial(get_charged_mesons, mesons=ps_mesons_01)
uncharged_01 = partial(get_uncharged_mesons, mesons=ps_mesons_01)

charged_02 = partial(get_charged_mesons, mesons=ps_mesons_02)
uncharged_02 = partial(get_uncharged_mesons, mesons=ps_mesons_02)

charged_03 = partial(get_charged_mesons, mesons=ps_mesons_03)
uncharged_03 = partial(get_uncharged_mesons, mesons=ps_mesons_03)

uncovariant_005 = Measurement(all_del_m_sq,
                              (charged_005, uncharged_005,
                               fit_params_uncovariant, fit_params_uncovariant),
                              simulation_kwargs={'method': MinuitFitter})

uncovariant_01 = Measurement(all_del_m_sq,
                             (charged_01, uncharged_01,
                              fit_params_uncovariant, fit_params_uncovariant),
                             simulation_kwargs={'method': MinuitFitter})

uncovariant_02 = Measurement(all_del_m_sq,
                             (charged_02, uncharged_02,
                              fit_params_uncovariant, fit_params_uncovariant),
                             simulation_kwargs={'method': MinuitFitter})

uncovariant_03 = Measurement(all_del_m_sq,
                             (charged_03, uncharged_03,
                              fit_params_uncovariant, fit_params_uncovariant),
                             simulation_kwargs={'method': MinuitFitter})

measurements = [
    {
        'name': 'ml_0.005', 'measurement': uncovariant_005,
        'template_name' : 'delmsq/index.html'
    },
    {
        'name': 'ml_0.01', 'measurement': uncovariant_01,
        'template_name' : 'delmsq/index.html'
    },
    {
        'name': 'ml_0.02', 'measurement': uncovariant_02,
        'template_name' : 'delmsq/index.html'
    },
    {
        'name': 'ml_0.03', 'measurement': uncovariant_03,
        'template_name' : 'delmsq/index.html'
    },
    ]