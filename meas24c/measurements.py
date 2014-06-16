from functools import partial

import numpy as np
from pyon.core.cache import cache_data

from delmsq.lib.fitting.delmsq import all_del_m_sq
from delmsq.lib.fitting.fit_mass import fit_masses, create_hadrons
from meas24c.models import ChargedMeson24c
from meas24c.views import get_charged_mesons, get_uncharged_mesons
from meas24c.plots import delmsq_plots, mass_plots_chg, mass_plots_unchg, \
    correlator_plots


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
ps_mesons = {m_l: all_ps_mesons(m_l=m_l) for m_l in light_masses}
uncharged_views = {}
charged_views = {}

for m_l in light_masses:
    cacher = cache_data("charged_func_{}".format(m_l))
    charged = cacher(partial(get_charged_mesons, ps_mesons[m_l]))

    cacher = cache_data("uncharged_func_{}".format(m_l))
    uncharged = cacher(partial(get_uncharged_mesons, ps_mesons[m_l]))

    uncharged_views[m_l] = uncharged
    charged_views[m_l] = charged

corr_meas_unch = {m_l: partial(create_hadrons, uncharged_views[m_l])
                  for m_l in light_masses}

corr_meas_ch = {m_l: partial(create_hadrons, charged_views[m_l])
                for m_l in light_masses}

uncovariant_mass = partial(fit_masses,
                           hadron_kwargs=fit_params_uncovariant)

uncovariant_mass_meas_unch = {}
uncovariant_mass_meas_ch = {}

for m_l in light_masses:
    cacher = cache_data('uncovar_mass_unch_func_{}'.format(m_l))
    uncovar_mass_unch = cacher(partial(uncovariant_mass, hadrons=corr_meas_unch[m_l]))

    cacher = cache_data('uncovar_mass_ch_func_{}'.format(m_l))
    uncovar_mass_ch = cacher(partial(uncovariant_mass, hadrons=corr_meas_ch[m_l]))

    uncovariant_mass_meas_unch[m_l] = uncovar_mass_unch
    uncovariant_mass_meas_ch[m_l] = uncovar_mass_ch


# uncovariant_mass_meas_unch = {m_l: partial(uncovariant_mass,
#                                            hadrons=corr_meas_unch[m_l])
#                               for m_l in light_masses}

# uncovariant_mass_meas_ch = {m_l: partial(uncovariant_mass,
#                                          hadrons=corr_meas_ch[m_l])
#                             for m_l in light_masses}

# covariant_delmsq = partial(all_del_m_sq,
#                            hadron1_kwargs=fit_params_covariant,
#                            hadron2_kwargs=fit_params_covariant)


uncovariant_delmsq_meas = {}

for m_l in light_masses:
    cacher = cache_data('uncovar_del_m_sq_{}'.format(m_l))
    uncovar_delmsq = cacher(partial(all_del_m_sq, charged_masses=uncovariant_mass_meas_ch[m_l],
                            uncharged_masses=uncovariant_mass_meas_unch[m_l]))
    uncovariant_delmsq_meas[m_l] = uncovar_delmsq


measurements = []

measurements += [{'name': 'corr_ml_{}_unch'.format(m_l),
                 'measurement': corr_meas_unch[m_l],
                 'template_name': 'correlator/index.html',
                 'plots': correlator_plots} for m_l in light_masses]

measurements += [{'name': 'corr_ml_{}_ch'.format(m_l),
                 'measurement': corr_meas_ch[m_l],
                 'template_name': 'correlator/index.html',
                 'plots': correlator_plots} for m_l in light_masses]

measurements += [{'name': 'mass_ml_{}_uncov_unch'.format(m_l),
                  'measurement': uncovariant_mass_meas_unch[m_l],
                  'template_name': 'mass_fit/index.html',
                  'plots': mass_plots_unchg} for m_l in light_masses]

measurements += [{'name': 'mass_ml_{}_uncov_ch'.format(m_l),
                  'measurement': uncovariant_mass_meas_ch[m_l],
                  'template_name': 'mass_fit/index.html',
                  'plots': mass_plots_chg} for m_l in light_masses]

measurements += [{'name': 'delmsq_ml_{}_uncov'.format(m_l),
                  'measurement': uncovariant_delmsq_meas[m_l],
                  'template_name': 'delmsq/index.html',
                  'plots': delmsq_plots} for m_l in light_masses]

# measurements += [{'name': 'ml_{}_cov'.format(m_l),
#                   'measurement': covariant_meas[m_l],
#                   'template_name': 'delmsq/index.html'}
#                  for m_l in light_masses]
