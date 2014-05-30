from functools import partial
import numpy as np
from pyon.runner.measurement import Measurement
from delmsq.lib.fitting import MinuitFitter, all_del_m_sq
from delmsq.views import get_charged_mesons, get_uncharged_mesons, ps_mesons


bnds = ((0., 1.), (0, None))
fit_params = dict(fit_range=np.array(range(7, 25+1)),
                  initial_value=dict(m=0.18, c=1.39432),
                  #initial_value=[0.18, 1.39432],
                  covariant=False,
                  bounds=bnds)

charged_view = partial(get_charged_mesons, mesons=ps_mesons)
uncharged_view = partial(get_uncharged_mesons, mesons=ps_mesons)

meas1 = Measurement(all_del_m_sq,
                    (charged_view, uncharged_view, fit_params, fit_params),
                    simulation_kwargs={'method': MinuitFitter})

measurements = [
    {
        'name': 'all', 'measurement': meas1,
        'template_name' : 'delmsq/index.html'
    },
    ]