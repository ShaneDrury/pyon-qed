import logging

from pyon.lib.fitting.base import FitParams
from pyon.lib.resampling import Jackknife


log = logging.getLogger(__name__)


def all_del_m_sq(charged_masses,
                 uncharged_masses):
    all_fit_params = {}
    charged = charged_masses()
    uncharged = uncharged_masses()

    for k, fp1 in charged.items():
        ml1, ml2, q1, q2 = k
        fp2 = uncharged[(ml1, ml2, 0, 0)]

        central_m1 = fp1.average_params
        central_m2 = fp2.average_params

        resampled_m1 = fp1.resampled_params
        resampled_m2 = fp2.resampled_params
        resampled_del_m2 = [del_m_sq(m1, m2)
                            for m1, m2 in zip(resampled_m1, resampled_m2)]

        central_del_m2 = del_m_sq(central_m1, central_m2)
        resampler = Jackknife(n=1)
        err_del_m2 = resampler.calculate_errors(central_del_m2,
                                                resampled_del_m2)

        log.debug("Mass-squared difference {}: {} {}"
                  .format(k, central_del_m2*1000, err_del_m2*1000))
        all_fit_params[k] = FitParams(central_del_m2, err_del_m2,
                                      resampled_del_m2)
    return all_fit_params


def del_m_sq(m1, m2):
    return m1*m1 - m2*m2

