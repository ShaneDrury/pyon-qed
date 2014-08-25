import logging

from pyon.lib.fitting.base import FitParams
from pyon.lib.fitting.common import fit_hadron
from pyon.lib.meson import PseudoscalarChargedMeson

from delmsq.lib.fitting.minuit import MinuitFitMethod

log = logging.getLogger(__name__)


def create_hadrons(data: 'callable', bin_size: int):
    dat = data()
    hadrons = {}
    for k, v in dat.items():

        m1, m2, q1, q2 = k
        h = PseudoscalarChargedMeson(
            v['data'],
            masses=(m1, m2),
            charges=(q1, q2),
            config_numbers=v['config_numbers']
        )

        if bin_size > 1:
            h.bin(bin_size)
        h.sort()
        h.fold()
        h.scale()
        hadrons[k] = h
    return hadrons


def fit_masses(hadrons: 'callable',
               hadron_kwargs: dict):
    all_fit_params = {}
    already_fit = {}
    had = hadrons()
    for k, h in had.items():
        if k not in already_fit:
            method = MinuitFitMethod
            fp = fit_hadron(h, method=method, **hadron_kwargs)
            already_fit[k] = fp
        else:
            fp = already_fit[k]
        central_mass = fp.average_params['m']
        err_mass = fp.errs['m']
        c2 = fp.average_params['chi_sq_dof']
        c2_err = fp.errs['chi_sq_dof']
        log.debug("Mass {}: {} {} {} {}".format(k, central_mass, err_mass, c2,
                                                c2_err))
        resampled_mass = fp.resampled_params['m']
        all_fit_params[k] = FitParams(central_mass, err_mass,
                                      resampled_mass)
    return all_fit_params
