# from pyon.lib.fitting import Fitter, registered_fitters
# from pyon.lib.register import Register
import logging
import minuit
from pyon.lib.fitting import Fitter, FitParams, fit_hadron
from pyon.lib.resampling import Jackknife
from qed.lib.fitfunc import make_chi_sq


#@Register(registered_fitters, 'minuit')
class MinuitFitter(Fitter):
    def fit_chi_sq(self, chi_sq, initial_value, **kwargs):
        #print(initial_value)
        m = minuit.Minuit(chi_sq, **initial_value)
        #m.tol = 0.0001
        m.migrad()
        return m.values

    @staticmethod
    def _generate_chi_sq_uncovariant(data, errors, fit_range, fit_func):
        return make_chi_sq(data, errors, fit_range)
        #return GenericChi2(data, errors, fit_range, fit_func)


def all_del_m_sq(charged_hadrons,
                    uncharged_hadrons,
                    hadron1_kwargs,
                    hadron2_kwargs,
                    method=None):
    all_fit_params = {}
    already_fit = {}
    for k, ch in charged_hadrons.items():
        m1, m2, q1, q2 = k
        unch = uncharged_hadrons[(m1, m2)]

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
        logging.debug("Mass {}: {} {}".format(k, central_m1, err_m1))
        logging.debug("Mass {}: {} {}".format((m1, m2), central_m2, err_m2))
        logging.debug("Mass-squared difference {}: {} {}"
                      .format(k, central_del_m2*1000, err_del_m2*1000))
        all_fit_params[k] = FitParams(central_del_m2, err_del_m2,
                                      resampled_del_m2)
    return all_fit_params


def del_m_sq(m1, m2):
    return m1*m1 - m2*m2


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
    # def is_bound(f):
    #     """test whether f is bound function"""
    #     return getattr(f, 'im_self', None) is not None
    #
    #
    # def describe(f):
    #     """extract function signature
    #
    #     ..seealso::
    #
    #         :ref:`function-sig-label`
    #     """
    #
    #     try:
    #         vnames = f.func_code.co_varnames
    #         #bound method and fake function will be None
    #         if is_bound(f):
    #             #bound method dock off self
    #             return list(vnames[1:f.func_code.co_argcount])
    #         else:
    #             #unbound and fakefunc
    #             return list(vnames[:f.func_code.co_argcount])
    #     except Exception as e:
    #         pass
    #         #using __call__ funccode
    #
    #     try:
    #         #vnames = f.__call__.func_code.co_varnames
    #         return list(f.__call__.func_code.co_varnames[1:f.__call__.func_code.co_argcount])
    #     except Exception as e:
    #         pass
    #
    #     try:
    #         return list(inspect.getargspec(f.__call__)[0][1:])
    #     except Exception as e:
    #         pass
    #
    #     try:
    #         return list(inspect.getargspec(f)[0])
    #     except Exception as e:
    #         pass
    #
    #     #now we are parsing __call__.__doc__
    #     #we assume that __call__.__doc__ doesn't have self
    #     #this is what cython gives
    #
    #     raise TypeError("Unable to obtain function signature")
    #     return None