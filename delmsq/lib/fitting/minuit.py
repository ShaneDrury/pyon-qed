from collections import defaultdict
import minuit

from pyon.lib.fitting.base import FitMethodBase
from pyon.lib.fitting.common import create_chi_sq_fitter
from pyon.lib.resampling import Jackknife


def fit_chi2_minuit(data, x_range=None, fit_func=None,
                    initial_value=None, covariant=False,
                    correlated=False, bounds=None, frozen=True):
    resampler = Jackknife(n=1)
    fit_method = MinuitFitMethod(fit_func)
    fitter = create_chi_sq_fitter(data, x_range, fit_func, initial_value,
                                  bounds, resampler, fit_method, frozen,
                                  covariant, correlated)
    return fitter


class MinuitFitMethod(FitMethodBase):
    def __init__(self, fit_func):
        self._fit_func = fit_func

    def fit(self, fit_objs, initial_value, bounds):
        fit_params = defaultdict(list)
        for fit_obj in fit_objs:
            args = ", ".join(fit_obj.args)
            template = "lambda {args!s}: fit_obj(*[{args!s}])"
            my_fit_obj = eval(template.format(args=args), {'fit_obj': fit_obj})
            m = minuit.Minuit(my_fit_obj, **initial_value)
            # m.fixed = {arg: 'False' for arg in fit_obj.args}
            m.tol = 0.0001
            # m.printMode = 1
            m.migrad()
            # m.values['chi_sq_dof'] = m.fval
            for k, v in m.values.items():
                fit_params[k].append(v)
            c2 = m.fval / (len(fit_obj.x_range) - len(fit_obj.args))  # THIS IS THE PROBLEMO
            # http://arxiv.org/pdf/1012.3754v1.pdf says it's N-P, not N-P+1
            fit_params['chi_sq_dof'].append(c2)
        return fit_params


        # initial_value = self._convert_initial_value(initial_value)
        # fit_params = defaultdict(list)
        # for fit_obj in fit_objs:
        #     # Scipy expects the function to have one argument, so this is a
        #     # wrapper to unpack those values and forward them to the fit_obj.
        #     to_fit = lambda p: fit_obj(*p)
        #
        #     out = minimize(to_fit, initial_value, bounds=bounds)
        #     for k, v in self._convert_fit_output(out).items():
        #         fit_params[k].append(v)
        #     self.fval.append(out.fun)
        #
        # return fit_params