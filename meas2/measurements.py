import numpy as np
from pyon.runner.measurement import Measurement
from delmsq.lib.fitting import MinuitFitter, all_del_m_sq
from delmsq.views import charged_mesons, uncharged_mesons

bnds = ((0., 1.), (0, None))
fit_params = dict(fit_range=np.array(range(7, 25+1)),
                  initial_value=dict(m=0.18, c=1.39432),
                  #initial_value=[0.18, 1.39432],
                  covariant=False,
                  bounds=bnds)

meas2 = Measurement(all_del_m_sq,
                    (charged_mesons, uncharged_mesons, fit_params, fit_params),
                    simulation_kwargs={'method': MinuitFitter})

measurements = [
    {
        'name': 'sub_meas1', 'measurement': meas2,
        'template_name' : 'delmsq/index.html'
    },
    {
        'name': 'sub_meas2', 'measurement': meas2,
        'template_name' : 'delmsq/index.html'
    },
    ]