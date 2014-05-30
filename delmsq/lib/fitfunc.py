__author__ = 'srd1g10'

from pyon.lib.fitfunction import pp_flat
import numpy as np


def make_chi_sq(data, errors, fit_range):
    """
    Work around for pyminuit - it's tied to pp_flat.
    """

    def chi_sq(m, c):
        ff = pp_flat(fit_range, m, c)
        return sum((data - ff)**2 / errors**2) / len(fit_range)
        # return sum([(data[t] - pp_flat(t, m, c))**2 / (errors[t])**2
        #                     for t in fit_range]) / len(fit_range)

    return chi_sq


def make_chi_sq_covar(data, inverse_covariance, fit_range):
    def chi_sq(m, c):
        ff = pp_flat(fit_range, m, c)
        # pared_data = np.array([data[t] for t in fit_range])
        v = np.array(ff - data)
        m = np.array(inverse_covariance)
        r = np.dot(m, v)
        c2 = np.dot(v, r)
        return c2 / len(fit_range)
    return chi_sq
