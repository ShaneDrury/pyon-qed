import logging
from jinja2 import Environment, PackageLoader
import numpy as np
from delmsq.lib.fitting import MinuitFitter, all_del_m_sq
from delmsq.views import charged_mesons, uncharged_mesons

template_env = Environment(loader=PackageLoader('delmsq', 'templates'))
template = template_env.get_template('index.html')


def del_m_sq_0042():
    logging.debug("Getting Charged")
    charged = charged_mesons()
    logging.debug("Getting Uncharged")
    uncharged = uncharged_mesons()

    charged_hadrons = {}
    for k, had in charged.items():
        had.sort()
        had.fold()
        had.scale()
        charged_hadrons[k] = had

    uncharged_hadrons = {}
    for k, had in uncharged.items():
        had.sort()
        had.fold()
        had.scale()
        uncharged_hadrons[k] = had

    bnds = ((0., 1.), (0, None))
    simulation_params = dict(fit_range=np.array(range(7, 25+1)),
                             initial_value=dict(m=0.18, c=1.39432),
                             #initial_value=[0.18, 1.39432],
                             covariant=False,
                             bounds=bnds)
    return all_del_m_sq(charged_hadrons, uncharged_hadrons,
                        simulation_params, simulation_params,
                        method=MinuitFitter)