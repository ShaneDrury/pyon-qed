import logging
import minuit

from pyon.core.cache import cache_data
from pyon.lib.fitting.base import FitParams
from pyon.lib.resampling import Jackknife
import numpy as np

from meas24c.measurements import covariant_delmsq_meas
from su2.lib.delmsq import del_m_sq_su2_fv_one
from su2.lib.fv import get_fv_corrections, get_fv_corrections_kaon_003, get_fv_corrections_kaon_002
from su2.lib.kaon import coefficients, get_y, filter_kaon_del_m_sq
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


@cache_data('get_qed_lec_pion_fv')
def get_qed_lec_pion_fv():
    num_lec = 190
    light_delmsq = {k: covariant_delmsq_meas[k] for k in (0.005, 0.01)}
    filtered_del_m_sq = filter_del_m_sq(light_delmsq)
    padded = pad(filtered_del_m_sq, num_lec)
    fit_func_params = [dict(B_0=b0,
                            F_0=f0,
                            mu_sq=musq,
                            L_4=l4,
                            L_5=l5,
                            mres=mmres)
                       for b0, f0, musq, l4, l5, mmres, *_ in get_pion_lec_su2()]
    fit_func = del_m_sq_su2_fv_one

    initial_value = dict(C=2.2*1e-7,
                         Y_2=1.63*1e-2,
                         Y_3=-11.85*1e-3,
                         Y_4=13.4*1e-3,
                         Y_5=2.06*1e-3,
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


# def filter_fv_kaon(fv_dict: dict, m_3: float) -> SymmetricDict:
#     d = {k: v for k, v in fv_dict.items() if k[1] == m_3}
#     return SymmetricDict(d.items())

def filter_fv_kaon(fv_dict: dict, m_3: float) -> dict:
    d = {}
    for k, v in fv_dict.items():
        if k[0] < k[1]:
            idx = 1
        elif k[0] > k[1]:
            idx = 0
        else:
            raise ValueError()
        if k[idx] == m_3:
            d[k] = v
    return d


def sort_vals_key(d: dict) -> dict:
    dd = {}
    for k, v in d.items():
        m1, m2, q1, q2, m_l = k
        if m2 < m1:
            m1, m2 = m2, m1
            q1, q2 = q2, q1
        new_key = (m1, m2, q1, q2, m_l)
        dd[new_key] = v
    return dd


def get_qed_lec_kaon_fv_002():
    return get_qed_lec_kaon_fv(get_fv_corrections_kaon_002(), 0.02)


def get_qed_lec_kaon_fv_003():
    return get_qed_lec_kaon_fv(get_fv_corrections_kaon_003(), 0.03)


def get_qed_lec_kaon_fv(fv_dict, m_s):
    num_lec = 190
    fit_func_params = [dict(B_0=b0,
                            F_0=f0,
                            mu_sq=musq,
                            L_4=l4,
                            L_5=l5,
                            mres=mmres)
                       for b0, f0, musq, l4, l5, mmres, *_ in get_pion_lec_su2()]
    qed_pion_lec = get_qed_lec_pion_fv()
    # fv_dict = get_fv_corrections_kaon_003()
    # get_fv_corrections_kaon_002()

    light_delmsq = {k: covariant_delmsq_meas[k]
                    for k in (0.005, 0.01, 0.02, 0.03)}
    filtered_del_m_sq = filter_kaon_del_m_sq(light_delmsq, m_s)
    padded = pad(filtered_del_m_sq, num_lec)
    padded = sort_vals_key(padded)
    x_range = list(padded.keys())

    ave_data = [v.average_params for k, v in padded.items()]
    data = [v.resampled_params for k, v in padded.items()]
    data = np.swapaxes(data, 0, 1)
    errs = [v.errs for k, v in padded.items()]
    avg_fit_func_params = {k: np.average([sample[k] for sample
                                          in fit_func_params])
                           for k in fit_func_params[0].keys()}

    fv_filtered = filter_fv_kaon(fv_dict, m_s)

    fv_list = [{xx: fv_filtered[xx][i] for xx in x_range}
               for i in range(len(data))]

    # fv_list = [fv_dict[xx] for xx in x_range]
    fv_avg = {xx: np.average(fv_filtered[xx], axis=0) for xx in x_range}
    b_vec_unscaled = np.array([get_y(xx, ave,
                                     qed_pion_lec['deltamres'].average_params,
                                     fv_avg[xx][3])
                               for xx, ave in zip(x_range,
                                                  ave_data)])  # b in ax=b
    jk_block = np.array(data)
    jk_block_T = [jk_block[:, i] for i in range(len(jk_block[1]))]
    all_y = []

    for i in range(len(jk_block_T)):  # 36
        this_del_m_sq = jk_block_T[i]
        this_x = x_range[i]
        this_correction = fv_list[i]
        this_y = [get_y(this_x, jj, dmres, this_correction[this_x][3])
                  for jj, dmres
                  in zip(this_del_m_sq,
                         qed_pion_lec['deltamres'].resampled_params)]
        all_y.append(this_y)

    resampler = Jackknife(n=1)
    jk_error_minus_dmres = [resampler.calculate_errors(bb, yy)
                            for bb, yy in zip(b_vec_unscaled, all_y)]

    b_vec = np.array([get_y(xx, ave, qed_pion_lec['deltamres'].average_params,
                            fv_avg[xx][3])/err
                      for xx, ave, err in zip(x_range, ave_data,
                                              jk_error_minus_dmres)])  # The b in ax=b

    a_vec = [coefficients(xx, avg_fit_func_params['mres'],
                          avg_fit_func_params['B_0'],
                          avg_fit_func_params['F_0'],
                          avg_fit_func_params['mu_sq'], fv_avg[xx][2])/err
             for xx, err in zip(x_range, jk_error_minus_dmres)]
    a_vec = np.array(a_vec)
    a_T = np.transpose(a_vec)
    m = np.linalg.lstsq(np.dot(a_T, a_vec), np.dot(a_T, b_vec))[0]

    ave_A_11 = m[0]
    ave_A_21 = m[1]
    ave_A_s11 = m[2]
    ave_A_s2 = m[3]
    ave_x_3 = m[4]
    ave_x_4 = m[5]
    ave_x_5 = m[6]
    ave_x_6 = m[7]
    ave_x_7 = m[8]
    ave_x_8 = m[9]

    """
    Jackknife fits
    """
    jk_A_11 = []
    jk_A_21 = []
    jk_A_s11 = []
    jk_A_s2 = []
    jk_x_3 = []
    jk_x_4 = []
    jk_x_5 = []
    jk_x_6 = []
    jk_x_7 = []
    jk_x_8 = []

    # fv_jk = np.swapaxes(fv_list, 0, 1)
    for i in range(num_lec):  # 190
        this_correction = fv_list[i]
        b_vec = np.array([get_y(xx, ave, qed_pion_lec['deltamres'].resampled_params[i],
                                this_correction[xx][3])/err
                          for xx, ave, err in zip(x_range, jk_block[i],
                                                  jk_error_minus_dmres)])  # The b in ax=b
        a_vec = [coefficients(xx, fit_func_params[i]['mres'],
                              fit_func_params[i]['B_0'],
                              fit_func_params[i]['F_0'],
                              fit_func_params[i]['mu_sq'],
                              this_correction[xx][2])/err
                 for xx, err in zip(x_range, jk_error_minus_dmres)]
        a_vec = np.array(a_vec)
        m = np.linalg.lstsq(a_vec, b_vec)[0]
        jk_A_11.append(m[0])
        jk_A_21.append(m[1])
        jk_A_s11.append(m[2])
        jk_A_s2.append(m[3])
        jk_x_3.append(m[4])
        jk_x_4.append(m[5])
        jk_x_5.append(m[6])
        jk_x_6.append(m[7])
        jk_x_7.append(m[8])
        jk_x_8.append(m[9])


    A_11_err = resampler.calculate_errors(ave_A_11, jk_A_11)
    A_21_err = resampler.calculate_errors(ave_A_21, jk_A_21)
    A_s11_err = resampler.calculate_errors(ave_A_s11, jk_A_s11)
    A_s2_err = resampler.calculate_errors(ave_A_s2, jk_A_s2)
    x_3_err = resampler.calculate_errors(ave_x_3, jk_x_3)
    x_4_err = resampler.calculate_errors(ave_x_4, jk_x_4)
    x_5_err = resampler.calculate_errors(ave_x_5, jk_x_5)
    x_6_err = resampler.calculate_errors(ave_x_6, jk_x_6)
    x_7_err = resampler.calculate_errors(ave_x_7, jk_x_7)
    x_8_err = resampler.calculate_errors(ave_x_8, jk_x_8)

    to_return = {'A_11': FitParams(ave_A_11, A_11_err, jk_A_11),
                 'A_21': FitParams(ave_A_21, A_21_err, jk_A_21),
                 'A_s11': FitParams(ave_A_s11, A_s11_err, jk_A_s11),
                 'A_s2': FitParams(ave_A_s2, A_s2_err, jk_A_s2),
                 'x_3': FitParams(ave_x_3, x_3_err, jk_x_3),
                 'x_4': FitParams(ave_x_4, x_4_err, jk_x_4),
                 'x_5': FitParams(ave_x_5, x_5_err, jk_x_5),
                 'x_6': FitParams(ave_x_6, x_6_err, jk_x_6),
                 'x_7': FitParams(ave_x_7, x_7_err, jk_x_7),
                 'x_8': FitParams(ave_x_8, x_8_err, jk_x_8),
                 }
    return to_return
