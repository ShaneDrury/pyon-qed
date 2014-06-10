import minuit
from pyon.lib.fitting.base import Fitter, FitMethod, create_generic_chi2_fitter
from pyon.lib.resampling import Jackknife
from pyon.lib.statistics import get_inverse_cov_matrix
from delmsq.lib.fitfunc import make_chi_sq, make_chi_sq_covar
import numpy as np


# def fit_chi2_minuit(data, fit_func=None, fit_range=None, initial_value=None, resampler=None,
#                     covariant=False, correlated=False, bounds=None):
#     resampler = resampler or Jackknife(n=1)
#     if covariant:
#         gen_err_func = lambda x: get_inverse_cov_matrix(x, correlated)
#         gen_fit_obj = make_chi_sq_covar
#     else:
#         def gen_err_func(x):
#             return np.std(x, axis=0) / len(x)
#         #gen_err_func = lambda x: np.std(x, axis=0) / len(x)
#         gen_fit_obj = make_chi_sq
#     fit_method = MinuitFitMethod
#     fitter = Fitter(data, fit_range, fit_func, initial_value, gen_err_func,
#                     gen_fit_obj, fit_method, resampler, bounds)
#     return fitter.fit()


def fit_chi2_minuit(data, fit_func=None, fit_range=None, initial_value=None,
                    resampler=None, covariant=False, correlated=False,
                    bounds=None):
    fitter = create_generic_chi2_fitter(data, MinuitFitMethod, fit_func,
                                        fit_range, initial_value, resampler,
                                        covariant, correlated, bounds)
    return fitter


class MinuitFitMethod(FitMethod):
    def fit(self, fit_obj, initial_value, bounds, fit_func):
        m = minuit.Minuit(fit_obj, **initial_value)
        #m.tol = 0.0001
        m.migrad()
        return m.values

        # If iminuit worked with Python3 this would be the solution:
        # class GenericChi2:
        #     def __init__(self, data, errors, fit_range, f):
        #         self.f = f
        #         args = describe(f)  #extract function signature
        #         self.func_code = Struct(
        #             co_varnames=args[1:],
        #             co_argcount=len(args)-1
        #         )
        #         self.data = data
        #         self.errors = errors
        #         self.fit_range = fit_range
        #
        #     def __call__(self, *args):
        #         return sum([(self.data[t] - self.f(t, *args))**2 / (self.errors[t])**2
        #                         for t in self.fit_range]) / len(self.fit_range)
        #
        #
        # class Struct:
        #     def __init__(self, **kwds):
        #         self.__dict__.update(kwds)
        #
        #     def __str__(self):
        #         return self.__dict__.__str__()
        #
        #     def __repr__(self):
        #         return self.__str__()
        #
        #     def __getitem__(self, s):
        #         return self.__dict__[s]
        #
        #