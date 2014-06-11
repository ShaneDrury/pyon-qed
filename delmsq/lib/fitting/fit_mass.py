import logging

from pyon.lib.fitting.base import fit_hadron, FitParams
from pyon.lib.meson import PseudoscalarChargedMeson

from delmsq.lib.fitting.minuit import MinuitFitMethod

log = logging.getLogger(__name__)


def create_hadrons(data):
    dat = data()
    hadrons = {}
    for k, v in dat.items():
        try:
            m1, m2, q1, q2 = k
        except ValueError:
            m1, m2 = k
            q1 = 0
            q2 = 0
        h = PseudoscalarChargedMeson(
            v['data'],
            masses=(m1, m2),
            charges=(q1, q2),
            config_numbers=v['config_numbers']
        )
        h.sort()
        h.fold()
        h.scale()
        hadrons[k] = h
    return hadrons


def fit_masses(hadrons,
               hadron_kwargs):
    method = MinuitFitMethod()
    all_fit_params = {}
    already_fit = {}
    had = hadrons()

    for k, h in had.items():
        if k not in already_fit:
            fp = fit_hadron(h, method=method, **hadron_kwargs)
            already_fit[k] = fp
        else:
            fp = already_fit[k]

        central_mass = fp.average_params['m']

        err_mass = fp.errs['m']
        log.debug("Mass {}: {} {}".format(k, central_mass, err_mass))
        resampled_mass = fp.resampled_params['m']
        all_fit_params[k] = FitParams(central_mass, err_mass,
                                      resampled_mass)
    return all_fit_params