from functools import partial

import numpy as np
from pyon.core.cache import cache_data

from delmsq.lib.delmsq import all_del_m_sq
from delmsq.lib.fitting.minuit import MinuitFitMethod
from meas24c.models import ChargedMeson24c
from meas24c.views import get_charged_mesons, get_uncharged_mesons


bnds = ((0., 1.), (0, None))
fit_params_uncovariant = dict(fit_range=np.array(range(9, 32+1)),
                              initial_value=dict(m=0.18, c=1.39432),
                              covariant=False,
                              bounds=bnds)

fit_params_covariant = fit_params_uncovariant.copy()
fit_params_covariant['covariant'] = True
fit_params_correlated = fit_params_covariant.copy()
fit_params_correlated['correlated'] = True

light_masses = [0.005, 0.01, 0.02]
# light_masses = [0.02]  # for testing
all_ps_mesons = ChargedMeson24c.objects.filter(source='GFWALL', sink='GAM_5')

# Don't care about order so dict is fine
ps_mesons = {m: all_ps_mesons(m_l=m) for m in light_masses}
uncharged_views = {}
charged_views = {}
for m_l, mesons in ps_mesons.items():
    @cache_data(cache_key="charged_{}".format(m_l))
    def charged():
        return get_charged_mesons(mesons)

    @cache_data(cache_key="uncharged_{}".format(m_l))
    def uncharged():
        return get_uncharged_mesons(mesons)
    uncharged_views[m_l] = uncharged
    charged_views[m_l] = charged


uncovariant_func = partial(all_del_m_sq,
                           hadron1_kwargs=fit_params_uncovariant,
                           hadron2_kwargs=fit_params_uncovariant,
                           method=MinuitFitMethod())

covariant_func = partial(all_del_m_sq,
                         hadron1_kwargs=fit_params_covariant,
                         hadron2_kwargs=fit_params_covariant,
                         method=MinuitFitMethod())

uncovariant_meas = {m_l: partial(uncovariant_func,
                                 uncharged_hadrons=uncharged_views[m_l],
                                 charged_hadrons=charged_views[m_l])
                    for m_l in light_masses}

covariant_meas = {m_l: partial(covariant_func,
                               uncharged_hadrons=uncharged_views[m_l],
                               charged_hadrons=charged_views[m_l])
                  for m_l in light_masses}

measurements = [{'name': 'ml_{}_uncov'.format(m_l),
                 'measurement': uncovariant_meas[m_l],
                 'template_name': 'delmsq/index.html'} for m_l in light_masses]

# measurements += [{'name': 'ml_{}_cov'.format(m_l),
#                   'measurement': covariant_meas[m_l],
#                   'template_name': 'delmsq/index.html'}
#                  for m_l in light_masses]
