import minuit

from pyon.lib.fitting.base import FitMethod, create_generic_chi2_fitter


def fit_chi2_minuit(data, x_range=None, fit_func=None, fit_range=None,
                    initial_value=None, resampler=None, covariant=False,
                    correlated=False, bounds=None):
    fitter = create_generic_chi2_fitter(data, x_range, MinuitFitMethod(),
                                        fit_func, fit_range, initial_value,
                                        resampler, covariant, correlated,
                                        bounds)
    return fitter


class MinuitFitMethod(FitMethod):
    def fit(self, fit_obj, initial_value, bounds):
        args = ", ".join(fit_obj.args)
        template = "lambda {args!s}: fit_obj(*[{args!s}])"
        my_fit_obj = eval(template.format(args=args), {'fit_obj': fit_obj})
        m = minuit.Minuit(my_fit_obj, **initial_value)
        # m.fixed = {arg: 'False' for arg in fit_obj.args}
        m.tol = 0.0001
        # m.printMode = 1
        m.migrad()
        m.values['chi_sq_dof'] = m.fval
        return m.values

    def _convert_initial_value(self, dic):
        return dic
