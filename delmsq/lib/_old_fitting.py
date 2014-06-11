import minuit

#from pyon.lib.fitting import Fitter
from pyon.lib.fitting.base import Fitter

from delmsq.lib.fitfunc import make_chi_sq, make_chi_sq_covar


class MinuitFitter(Fitter):
    def fit_chi_sq(self, chi_sq, initial_value, **kwargs):
        m = minuit.Minuit(chi_sq, **initial_value)
        #m.tol = 0.0001
        m.migrad()
        return m.values

    @staticmethod
    def _generate_chi_sq_uncovariant(data, errors, fit_range, fit_func):
        return make_chi_sq(data, errors, fit_range)
        #return GenericChi2(data, errors, fit_range, fit_func)

    @staticmethod
    def _generate_chi_sq_covariant(data, inverse_covariance, fit_range,
                                   fit_func):
        return make_chi_sq_covar(data, inverse_covariance, fit_range)


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