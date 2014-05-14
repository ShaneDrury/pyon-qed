import logging
import numpy as np
from delmsq.lib.fitting import MinuitFitter, all_del_m_sq
from delmsq.views import charged_mesons, uncharged_mesons


def del_m_sq_0042():
    logging.debug("Getting Charged")
    charged_hadrons = charged_mesons()

    logging.debug("Getting Uncharged")
    uncharged_hadrons = uncharged_mesons()

    bnds = ((0., 1.), (0, None))
    fit_params = dict(fit_range=np.array(range(7, 25+1)),
                      initial_value=dict(m=0.18, c=1.39432),
                      #initial_value=[0.18, 1.39432],
                      covariant=False,
                      bounds=bnds)
    return all_del_m_sq(charged_hadrons, uncharged_hadrons,
                        fit_params, fit_params, method=MinuitFitter)
