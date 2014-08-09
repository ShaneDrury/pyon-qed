from functools import partial

from pyon.lib.fitting.common import Fitter, ErrorGenerator, \
    ChiSqFitObjectGenerator
from pyon.lib.resampling import Jackknife
from pyon.lib.structs.errors import OneErrorGeneratorBase
import numpy as np

from delmsq.lib.fitting.minuit import MinuitFitMethod


def fit_chi2_minuit_delmsq(jackknife_data, x_range=None, fit_func=None,
                           initial_value=None, errs=None, fit_func_params=None,
                           central_data=None):

    resampler = Jackknife(n=1)  # TODO: Maybe change this to a dummy resampler
    fit_object_generator = ChiSqFitObjectGenerator()
    one_err_generator = FrozenOneErrorGenerator(errs)
    error_generator = ErrorGenerator(one_err_generator, frozen=True)

    fitter = DelMSqFitter(jackknife_data, x_range, fit_func, initial_value, None,
                          resampler, error_generator, fit_object_generator,
                          MinuitFitMethod(fit_func), fit_func_params,
                          central_data)
    return fitter


class FrozenOneErrorGenerator(OneErrorGeneratorBase):
    def __init__(self, err):
        self._err = err

    def generate(self, data):
        return self._err


# class DelMSqChi2(GenericChi2):
#     """
#     Remove x_range scaling
#     """
#     def __call__(self, *args):
#         ff = self.fit_func(self.x_range, *args)
#         return sum(((self.data - ff) / self.errors)**2)


class DelMSqFitter(Fitter):
    """
    This is a refinement of the existing Fitter class.
    It uses a different fit function for each jackknife sample.
    TODO: This is pretty different from the regular Fitter so maybe just
    make a new class?
    """

    def __init__(self, data, x_range, fit_func, initial_value, bounds,
                 resampler, error_generator, fit_object_generator, fit_method,
                 fit_func_params, central_data):
        self._fit_func_params = fit_func_params
        self._central_data = central_data
        super().__init__(data, x_range, fit_func, initial_value, bounds,
                         resampler, error_generator, fit_object_generator,
                         fit_method)

    def _prepare_fit_funcs(self):
        self._fit_funcs = [partial(self._fit_func_base, **kwargs)
                           for kwargs in self._fit_func_params]
        avg_fit_func_params = {k: np.average([sample[k] for sample
                                              in self._fit_func_params])
                               for k in self._fit_func_params[0].keys()}
        self._central_fit_func = partial(self._fit_func_base,
                                         **avg_fit_func_params)

    def _prepare_data(self):
        pass  # Don't need to do x_range in this case

    def _prepare_central_fit_obj(self):
        self._central_fit_obj = self._fit_obj_gen.generate(
            self._central_data,
            self._err_gen.generate_central_error(self._central_data),
            self._central_fit_func, self._x_range)

    def _prepare_fit_objs(self, ave_resampled, errors):
        """
        Note, ave_resampled isn't used, but self._data is instead.
        """
        self._fit_objects = [self._fit_obj_gen.generate(sample, err,
                                                        ff,
                                                        self._x_range)
                             for sample, err, ff in zip(self._data, errors,
                                                        self._fit_funcs)]


    def _prepare_ave_resampled(self, resampled_data):
        return self._central_data


    # class DelMSqFitter(FitterBase):
    #
    # def __init__(self, data=None, x_range=None, fit_range=None, fit_func=None,
    #              initial_value=None, gen_err_func=None, gen_fit_obj=None,
    #              fit_method=None, resampler=None, bounds=None, frozen=True):
    #     self.data = np.array(data)
    #     self.x_range = x_range
    #     self.fit_range = fit_range
    #     self.fit_func = fit_func
    #     self.initial_value = initial_value
    #     self.gen_err_func = gen_err_func
    #     self.gen_fit_obj = gen_fit_obj
    #     self.fit_method = fit_method
    #     self.resampler = resampler
    #     self.frozen = frozen
    #     self.errors = self._gen_errs()
    #     self.bounds = bounds
    #
    # def _gen_errs(self):
    #     errors = self.gen_err_func(self.data)
    #     return errors
    #
    # def _get_average_params(self):
    #     average_fit_obj = self.gen_fit_obj(self.data,
    #                                        self.errors,
    #                                        self.x_range,
    #                                        self.fit_func,
    #                                        fit_range=self.fit_range)
    #     self.average_fit_obj = average_fit_obj
    #     average_params = self.fit_method.fit(average_fit_obj,
    #                                          self.initial_value, self.bounds)
    #     average_params['chi_sq_dof'] = self._chi_sq_dof(average_params['chi_sq_dof'])
    #     return average_params
