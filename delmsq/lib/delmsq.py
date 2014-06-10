import logging

from pyon.lib.fitting.base import fit_hadron, FitParams
from pyon.lib.meson import PseudoscalarChargedMeson
from pyon.lib.resampling import Jackknife


__author__ = 'srd1g10'
log = logging.getLogger(__name__)


def all_del_m_sq(charged_hadrons,
                 uncharged_hadrons,
                 hadron1_kwargs,
                 hadron2_kwargs,
                 method=None):
    all_fit_params = {}
    already_fit = {}
    charged = charged_hadrons()
    uncharged = uncharged_hadrons()

    for k, v in charged.items():
        m1, m2, q1, q2 = k
        ch = PseudoscalarChargedMeson(
            v['data'],
            masses=(m1, m2),
            charges=(q1, q2),
            config_numbers=v['config_numbers']
        )
        ch.sort()
        ch.fold()
        ch.scale()

        unch_v = uncharged[(m1, m2)]
        unch = PseudoscalarChargedMeson(
            unch_v['data'],
            masses=(m1, m2),
            charges=(0, 0),
            config_numbers=unch_v['config_numbers']
        )
        unch.sort()
        unch.fold()
        unch.scale()
        if k not in already_fit:
            fp1 = fit_hadron(ch, method=method, **hadron1_kwargs)
            already_fit[k] = fp1
        else:
            fp1 = already_fit[k]

        if (m1, m2) not in already_fit:
            fp2 = fit_hadron(unch, method=method, **hadron2_kwargs)
            already_fit[(m1, m2)] = fp2
        else:
            fp2 = already_fit[(m1, m2)]

        central_m1 = fp1.average_params['m']
        central_m2 = fp2.average_params['m']

        err_m1 = fp1.errs['m']
        err_m2 = fp2.errs['m']

        resampled_m1 = fp1.resampled_params['m']
        resampled_m2 = fp2.resampled_params['m']
        resampled_del_m2 = [del_m_sq(m1, m2)
                            for m1, m2 in zip(resampled_m1, resampled_m2)]

        central_del_m2 = del_m_sq(central_m1, central_m2)
        resampler = Jackknife(n=1)
        err_del_m2 = resampler.calculate_errors(central_del_m2,
                                                resampled_del_m2)
        log.debug("Mass {}: {} {}".format(k, central_m1, err_m1))
        log.debug("Mass {}: {} {}".format((m1, m2), central_m2, err_m2))
        log.debug("Mass-squared difference {}: {} {}"
                  .format(k, central_del_m2*1000, err_del_m2*1000))
        all_fit_params[k] = FitParams(central_del_m2, err_del_m2,
                                      resampled_del_m2)
    return all_fit_params


def del_m_sq(m1, m2):
    return m1*m1 - m2*m2

