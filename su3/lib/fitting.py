from functools import partial

from pyon.lib.fitting.base import Fitter, GenericChi2
from pyon.lib.resampling import Jackknife
import numpy as np

from delmsq.lib.fitting.minuit import MinuitFitMethod


def fit_chi2_minuit_delmsq(data, x_range=None, fit_func=None, fit_range=None,
                           initial_value=None, bounds=None, frozen=True):

    resampler = Jackknife(n=1)
    gen_err_func = partial(np.std, axis=0)
    gen_fit_obj = make_delmsq_chi2

    fitter = Fitter(data, x_range, fit_range, fit_func, initial_value,
                    gen_err_func, gen_fit_obj, MinuitFitMethod(), resampler,
                    bounds, frozen)
    return fitter


def make_delmsq_chi2(data, errors, x_range, fit_func, fit_range=None):
    if fit_range is not None:
        data = data[fit_range]
        errors = errors[fit_range]
    chi_sq = DelMSqChi2(data, errors, x_range, fit_func)
    return chi_sq


class DelMSqChi2(GenericChi2):
    """
    Remove x_range scaling
    """
    def __call__(self, *args):
        ff = self.fit_func(self.x_range, *args)
        return sum((self.data - ff)**2 / self.errors**2)