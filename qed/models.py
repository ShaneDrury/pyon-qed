"""
Define your models here. These are the things that will be used to analyse the
data.
"""
from django.db import models
#from picklefield import PickledObjectField


class Iwasaki32cChargedMeson(models.Model):
    source = models.CharField(max_length=20)
    sink = models.CharField(max_length=20)
    mass_1 = models.FloatField()
    mass_2 = models.FloatField()
    charge_1 = models.IntegerField()
    charge_2 = models.IntegerField()
    config_number = models.IntegerField()


class TimeSlice(models.Model):
    t = models.IntegerField()
    re = models.FloatField()
    im = models.FloatField()
    meson = models.ForeignKey(Iwasaki32cChargedMeson, related_name='data')

    # import logging
    # from pyon import Model
    # from pyon.lib.fitting import fit_hadron, FitParams, registered_fitters
    # from pyon.lib.resampling import Jackknife
    #
    #
    # #@app.register_model('all del m sq')
    # class AllDelMSq(Model):
    #
    #     def __init__(self, fitter=None):
    #         #self.fitter = registered_fitters['minuit']
    #         #self.fitter = None
    #         self.fitter = fitter
    #
    #     def fit_all_hadrons(self, charged_hadrons,
    #                         uncharged_hadrons,
    #                         hadron1_kwargs,
    #                         hadron2_kwargs):
    #         all_fit_params = {}
    #         already_fit = {}
    #         for k, ch in charged_hadrons.items():
    #             m, q = k
    #             unch = uncharged_hadrons[m]
    #
    #             if k not in already_fit:
    #                 fp1 = self.fit_hadron(ch, **hadron1_kwargs)
    #                 already_fit[k] = fp1
    #             else:
    #                 fp1 = already_fit[k]
    #
    #             if m not in already_fit:
    #                 fp2 = self.fit_hadron(unch, **hadron2_kwargs)
    #                 already_fit[m] = fp2
    #             else:
    #                 fp2 = already_fit[m]
    #
    #             central_m1 = fp1.average_params['m']
    #             central_m2 = fp2.average_params['m']
    #
    #             err_m1 = fp1.errs['m']
    #             err_m2 = fp2.errs['m']
    #
    #             resampled_m1 = fp1.resampled_params['m']
    #             resampled_m2 = fp2.resampled_params['m']
    #             resampled_del_m2 = [self.del_m_sq(m1, m2)
    #                                 for m1, m2 in zip(resampled_m1, resampled_m2)]
    #
    #             central_del_m2 = self.del_m_sq(central_m1, central_m2)
    #             resampler = Jackknife(n=1)
    #             err_del_m2 = resampler.calculate_errors(central_del_m2,
    #                                                     resampled_del_m2)
    #             logging.debug("Mass {}: {} {}".format(k, central_m1, err_m1))
    #             logging.debug("Mass {}: {} {}".format(m, central_m2, err_m2))
    #             logging.debug("Mass-squared difference {}: {} {}"
    #                           .format(k, central_del_m2*1000, err_del_m2*1000))
    #             all_fit_params[k] = FitParams(central_del_m2, err_del_m2,
    #                                           resampled_del_m2)
    #         return all_fit_params
    #
    #     @staticmethod
    #     def del_m_sq(m1, m2):
    #         return m1*m1 - m2*m2
    #
    #     def fit_hadron(self, hadron, **kwargs):
    #         return fit_hadron(hadron, method=self.fitter, **kwargs)
    #
    #     def main(self):
    #         return self.fit_all_hadrons
    #
    #
    # #@register.model('msqdiff')  unused
    # class DelMSq(Model):
    #     def fit_hadrons(self, hadron1, hadron2, hadron1_kwargs, hadron2_kwargs):
    #         fp1 = self.fit_hadron(hadron1, **hadron1_kwargs)
    #         fp2 = self.fit_hadron(hadron2, **hadron2_kwargs)
    #         central_m1 = fp1.average_params['m']
    #         central_m2 = fp2.average_params['m']
    #         resampled_m1 = fp1.resampled_params['m']
    #         resampled_m2 = fp2.resampled_params['m']
    #         resampled_del_m2 = [self.del_m_sq(m1, m2)
    #                             for m1, m2 in zip(resampled_m1, resampled_m2)]
    #         central_del_m2 = self.del_m_sq(central_m1, central_m2)
    #         resampler = Jackknife(n=1)
    #         err_del_m2 = resampler.calculate_errors(central_del_m2,
    #                                                 resampled_del_m2)
    #         return FitParams(central_del_m2, err_del_m2, resampled_del_m2)
    #
    #     @staticmethod
    #     def del_m_sq(m1, m2):
    #         return m1*m1 - m2*m2
    #
    #     @staticmethod
    #     def fit_hadron(hadron, **kwargs):
    #         return fit_hadron(hadron, **kwargs)
    #
    #     def main(self):
    #         return self.fit_hadrons