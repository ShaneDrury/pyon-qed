from pyon.lib.fitting.base import Fitter, GenericChi2

from pyon.lib.resampling import Jackknife

from delmsq.lib.fitting.minuit import MinuitFitMethod




# class DelMSqFitter(Fitter):
#     def _gen_errs(self):
#         if self.frozen:
#             errs = self.gen_err_func(self.data)
#             errors = [errs for _ in self.data]
#         else:
#             errors = [self.gen_err_func(sample) for sample in
#                       self.resampler.generate_samples(self.data)]
#         return errors


def fit_chi2_minuit_delmsq(data, x_range=None, fit_func=None, fit_range=None,
                           initial_value=None, bounds=None, frozen=True,
                           errs=None):

    resampler = Jackknife(n=1)
    # gen_err_func = partial(np.std, axis=0)
    gen_err_func = lambda x: errs
    gen_fit_obj = make_delmsq_chi2
    fitter = DelMSqFitter(data, x_range, fit_range, fit_func, initial_value,
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
        return sum(((self.data - ff) / self.errors)**2)


class DelMSqFitter(Fitter):

    def _gen_errs(self):
        errors = self.gen_err_func(self.data)
        return errors

    def _get_average_params(self):
        average_fit_obj = self.gen_fit_obj(self.data,
                                           self.errors,
                                           self.x_range,
                                           self.fit_func,
                                           fit_range=self.fit_range)
        self.average_fit_obj = average_fit_obj
        average_params = self.fit_method.fit(average_fit_obj,
                                             self.initial_value, self.bounds)
        average_params['chi_sq_dof'] = self._chi_sq_dof(average_params['chi_sq_dof'])
        return average_params