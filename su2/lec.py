import logging
import minuit

from pyon.lib.fitting.base import FitParams
from pyon.lib.resampling import Jackknife
import numpy as np

from meas24c.measurements import covariant_delmsq_meas
from su2.lib.delmsq import del_m_sq_su2_fv_one
from su2.lib.fv import get_fv_corrections
from su2.models import PionLECSU2
from su3.lib.statistics import pad
from su3.views import filter_del_m_sq


log = logging.getLogger(__name__)


def get_pion_lec_su2():
    all_lec = PionLECSU2.objects.order_by('config_number')
    jk_f0 = [qs.F0 for qs in all_lec]
    jk_b0 = [qs.B0 for qs in all_lec]
    jk_miu = [qs.miu**2 for qs in all_lec]
    jk_l4 = [qs.L4 for qs in all_lec]
    jk_l5 = [qs.L5 for qs in all_lec]
    jk_m_res = [qs.m_res for qs in all_lec]
    jk_ls = [qs.LS for qs in all_lec]
    jk_l64 = [qs.L64 for qs in all_lec]
    jk_l85 = [qs.L85 for qs in all_lec]

    return zip(jk_b0, jk_f0, jk_miu, jk_l4, jk_l5, jk_m_res, jk_ls, jk_l64,
               jk_l85)


def get_qed_lec_pion_fv():
    NUM_LEC = 190
    light_delmsq = {k: covariant_delmsq_meas[k] for k in (0.005, 0.01)}
    filtered_del_m_sq = filter_del_m_sq(light_delmsq)
    padded = pad(filtered_del_m_sq, NUM_LEC)
    fit_func_params = [dict(B_0=b0,
                            F_0=f0,
                            mu_sq=musq,
                            L_4=l4,
                            L_5=l5,
                            mres=mmres)
                       for b0, f0, musq, l4, l5, mmres, *_ in get_pion_lec_su2()]
    fit_func = del_m_sq_su2_fv_one

    initial_value = dict(C=2.2*1e-7,
                         Y2=1.63*1e-2,
                         Y3=-11.85*1e-3,
                         Y4=13.4*1e-3,
                         Y5=2.06*1e-3,
                         deltamres=5.356*1e-3)

    x_range = list(padded.keys())

    ave_data = [v.average_params for k, v in padded.items()]
    data = [v.resampled_params for k, v in padded.items()]
    data = np.swapaxes(data, 0, 1)
    errs = [v.errs for k, v in padded.items()]
    avg_fit_func_params = {k: np.average([sample[k] for sample
                                          in fit_func_params])
                           for k in fit_func_params[0].keys()}

    fv_dict = get_fv_corrections()
    fv_list = [{xx: fv_dict[xx][i] for xx in x_range} for i in range(len(data))]

    # fv_list = [fv_dict[xx] for xx in x_range]
    fv_avg = {xx: np.average(fv_dict[xx], axis=0) for xx in x_range}

    def min_1_3(lec, corrections, data, errors):
        def chi_sq(C, Y_2, Y_3, Y_4, Y_5, deltamres):
            c2 = 0.
            for xx, y, err in zip(x_range, data, errors):
                fv = corrections[xx]
                lec['correction'] = fv[1]
                ff = fit_func(xx, C, Y_2, Y_3, Y_4, Y_5, deltamres, **lec)
                c2 += ((ff - y + fv[0]) / err)**2
            return c2

        m = minuit.Minuit(chi_sq)
        # guess = dict(C=2.2*1e-7, Y_2=1.63*1e-2, Y_3=-11.85*1e-3, Y_4=13.4*1e-3,
        #              Y_5=2.06*1e-3, deltamres=5.356*1e-3)
        m.values = initial_value
        # m.printMode = 0
        m.migrad()
        return m.values['C'], m.values['Y_2'], m.values['Y_3'], \
               m.values['Y_4'], m.values['Y_5'], m.values['deltamres']

    central_C, central_Y_2, central_Y_3, central_Y_4, central_Y_5, \
    central_deltamres = min_1_3(avg_fit_func_params, fv_avg, ave_data, errs)
    log.debug("Central {}".format((central_C, central_Y_2, central_Y_3,
                                   central_Y_4, central_Y_5,
                                   central_deltamres)))
    jk_C = []
    jk_Y_2 = []
    jk_Y_3 = []
    jk_Y_4 = []
    jk_Y_5 = []
    jk_deltamres = []
    for jk_lec, jk_data, jk_fv in zip(fit_func_params, data, fv_list):
        c, y2, y3, y4, y5, dmres = min_1_3(jk_lec, jk_fv, jk_data, errs)
        jk_C.append(c)
        jk_Y_2.append(y2)
        jk_Y_3.append(y3)
        jk_Y_4.append(y4)
        jk_Y_5.append(y5)
        jk_deltamres.append(dmres)


    resampler = Jackknife(n=1)
    C_err = resampler.calculate_errors(central_C, jk_C)
    Y_2_err = resampler.calculate_errors(central_Y_2, jk_Y_2)
    Y_3_err = resampler.calculate_errors(central_Y_3, jk_Y_3)
    Y_4_err = resampler.calculate_errors(central_Y_4, jk_Y_4)
    Y_5_err = resampler.calculate_errors(central_Y_5, jk_Y_5)
    deltamres_err = resampler.calculate_errors(central_deltamres, jk_deltamres)

    to_return = {'C': FitParams(central_C, C_err, jk_C),
                 'Y_2': FitParams(central_Y_2, Y_2_err, jk_Y_2),
                 'Y_3': FitParams(central_Y_3, Y_3_err, jk_Y_3),
                 'Y_4': FitParams(central_Y_4, Y_4_err, jk_Y_4),
                 'Y_5': FitParams(central_Y_5, Y_5_err, jk_Y_5),
                 'deltamres': FitParams(central_deltamres, deltamres_err,
                                        jk_deltamres)}
    return to_return
