import logging

from pyon.lib.fitting.base import FitParams
import numpy as np
from pyon.lib.fitting.common import map_fit_params_to_dict

from meas24c.measurements import covariant_delmsq_meas
from su3.lib.fitting import fit_chi2_minuit_delmsq
from su3.models import PionLECSU3
from su3.views import filter_del_m_sq
from su3.lib.delmsq import del_m_sq_su3


log = logging.getLogger(__name__)




def pad(samples, num_lec):
    """
    Build super jackknife block.
    There are 190 QCD LECs, but only 98 + 45 = 143 delta m square jk samples
    Fill the rest with the average of them i.e.:
    Q0,   Q1,   Q2,   Q3,   Q4
    A0,   A1,   Aave, Aave, Aave
    Bave, Bave, Bave, B0,   B1

    Where Q are the QCD LEC jackknife samples, and A and B are the 0.005 and
    0.01 jackknife samples.

    000-097: m0.005 is from data, m0.01 is from ave.
    098-100: both m0.005 and m0.01 are from ave.
    101-145: m0.005 is from ave, m0.01 is from data.
    146-189: both m0.005 and m0.01 are from ave.
    """
    new_dict = {}
    for k, v in samples.items():
        ml1, ml2, q1, q2, m_l = k
        if m_l == 0.005:
            new_v = v.resampled_params
            for i in range(num_lec - len(v.resampled_params)):
                new_v.append(v.average_params)
            new_dict[k] = FitParams(v.average_params, v.errs, new_v)
        elif m_l == 0.01:
            new_v = []
            for i in range(100):  # Matches Ran's Code
                new_v.append(v.average_params)
            new_v += v.resampled_params

            for i in range(num_lec - len(new_v)):
                new_v.append(v.average_params)

            new_dict[k] = FitParams(v.average_params, v.errs, new_v)
        else:
            raise ValueError("m_l not 0.005 or 0.01")
    return new_dict


def find_qed_lec():
    NUM_LEC = 190
    light_delmsq = {k: covariant_delmsq_meas[k] for k in (0.005, 0.01)}
    filtered_del_m_sq = filter_del_m_sq(light_delmsq)
    all_lec = PionLECSU3.objects.order_by('config_number')
    jk_f0 = [qs.F0 for qs in all_lec]
    jk_b0 = [qs.B0 for qs in all_lec]
    jk_miu = [qs.miu**2 for qs in all_lec]
    jk_l4 = [qs.L4 for qs in all_lec]
    jk_l5 = [qs.L5 for qs in all_lec]
    jk_m_res = [qs.m_res for qs in all_lec]

    padded = pad(filtered_del_m_sq, NUM_LEC)

    fit_func_params = [dict(B0=b0,
                            F0=f0,
                            musq=musq,
                            L4=l4,
                            L5=l5,
                            mres=mres)
                       for b0, f0, musq, l4, l5, mres in zip(jk_b0, jk_f0,
                                                             jk_miu, jk_l4,
                                                             jk_l5, jk_m_res)]
    fit_func = del_m_sq_su3

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

    fitter = fit_chi2_minuit_delmsq(data, fit_func=fit_func,
                                    x_range=x_range,
                                    initial_value=initial_value,
                                    errs=errs, fit_func_params=fit_func_params,
                                    central_data=ave_data)
    fp = fitter.fit()
    to_return = map_fit_params_to_dict(fp)
    return to_return

measurements = [
    {
        'name': 'qed_lec_fv',
        'measurement': find_qed_lec,
        'template_name': 'su3/index.html',
    },
    # {
    #     'name': 'mu_md_fv',
    #     'measurement': find_light_masses_su3,
    #     'template_name': 'su3/mud.html',
    # }
]
