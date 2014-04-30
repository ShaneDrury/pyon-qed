__author__ = 'srd1g10'

from pyon.lib.fitfunction import pp_flat


def make_chi_sq(data, errors, fit_range):
    """
    Work around for pyminuit
    """

    def chi_sq(m, c):
        ff = pp_flat(fit_range, m, c)
        return sum((data - ff)**2 / errors**2) / len(fit_range)
        # return sum([(data[t] - pp_flat(t, m, c))**2 / (errors[t])**2
        #                     for t in fit_range]) / len(fit_range)

    return chi_sq