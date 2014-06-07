from functools import partial
import numpy as np
from delmsq.lib.delmsq import all_del_m_sq
from delmsq.lib.fitting import MinuitFitter
from delmsq.views import get_charged_mesons, get_uncharged_mesons, ps_mesons


bnds = ((0., 1.), (0, None))
fit_params = dict(fit_range=np.array(range(7, 25+1)),
                  initial_value=dict(m=0.18, c=1.39432),
                  #initial_value=[0.18, 1.39432],
                  covariant=False,
                  bounds=bnds)

charged_view = partial(get_charged_mesons, mesons=ps_mesons)
uncharged_view = partial(get_uncharged_mesons, mesons=ps_mesons)


meas1 = partial(all_del_m_sq,
                uncharged_hadrons=uncharged_view,
                charged_hadrons=charged_view,
                hadron1_kwargs=fit_params,
                hadron2_kwargs=fit_params,
                method=MinuitFitter)

measurements = [
    {
        'name': 'all', 'measurement': meas1,
        'template_name' : 'delmsq/index.html'
    },
    ]