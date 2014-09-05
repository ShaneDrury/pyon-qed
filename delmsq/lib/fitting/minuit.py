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

    def fit(self, fit_objs: list, initial_value: dict, bounds: dict):
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
            for k, v in m.values.items():
                fit_params[k].append(v)
            c2 = m.fval / fit_obj.dof()
            # http://arxiv.org/pdf/1012.3754v1.pdf says it's N-P, not N-P+1
            fit_params['chi_sq_dof'].append(c2)
        return fit_params
