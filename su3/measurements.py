import logging
import minuit

from pyon.core.cache import cache_data
from pyon.lib.fitting.base import FitParams
import numpy as np
from pyon.lib.fitting.common import map_fit_params_to_dict
from pyon.lib.resampling import Jackknife

from meas24c.measurements import covariant_delmsq_meas
from su3.lib.fitting import fit_chi2_minuit_delmsq
from su3.models import PionLECSU3
from su3.views import filter_del_m_sq
from su3.lib.delmsq import del_m_sq_su3, m_13_sq


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


def get_pion_lec_su3():
    """
    QCD Pion LECs for SU3
    """
    all_lec = PionLECSU3.objects.order_by('config_number')
    jk_f0 = [qs.F0 for qs in all_lec]
    jk_b0 = [qs.B0 for qs in all_lec]
    jk_miu = [qs.miu**2 for qs in all_lec]
    jk_l4 = [qs.L4 for qs in all_lec]
    jk_l5 = [qs.L5 for qs in all_lec]
    jk_m_res = [qs.m_res for qs in all_lec]
    jk_ls = [qs.LS for qs in all_lec]
    jk_l64 = [qs.L64 for qs in all_lec]
    jk_l85 = [qs.L85 for qs in all_lec]

    return zip(jk_b0, jk_f0, jk_miu, jk_l4, jk_l5, jk_m_res, jk_ls, jk_l64, jk_l85)


@cache_data('find_qed_lec')
def find_qed_lec():
    NUM_LEC = 190
    light_delmsq = {k: covariant_delmsq_meas[k] for k in (0.005, 0.01)}
    filtered_del_m_sq = filter_del_m_sq(light_delmsq)
    padded = pad(filtered_del_m_sq, NUM_LEC)
    fit_func_params = [dict(B0=b0,
                            F0=f0,
                            musq=musq,
                            L4=l4,
                            L5=l5,
                            mres=mres)
                       for b0, f0, musq, l4, l5, mres, *_ in get_pion_lec_su3()]
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
    avg_fit_func_params = {k: np.average([sample[k] for sample
                                          in fit_func_params])
                           for k in fit_func_params[0].keys()}

    fitter = fit_chi2_minuit_delmsq(data, fit_func=fit_func,
                                    x_range=x_range,
                                    initial_value=initial_value,
                                    errs=errs, fit_func_params=fit_func_params,
                                    avg_fit_func_params=avg_fit_func_params,
                                    central_data=ave_data)
    fp = fitter.fit()
    log.debug("Ave: {}".format(fp.average_params))
    log.debug("Errs: {}".format(fp.errs))
    to_return = map_fit_params_to_dict(fp)
    return to_return


def find_light_masses_su3():
    qed_lecs = find_qed_lec()
    qed_lecs.pop('chi_sq_dof')
    z_m = 1.5458  # Renormalization constant
    fit_func = m_13_sq
    fit_func_params = [dict(B0=b0,
                            F0=f0,
                            musq=musq,
                            L4=l4,
                            L5=l5,
                            mres=mres,
                            LS=ls,
                            L64=l64,
                            L85=l85)
                       for b0, f0, musq, l4, l5, mres, ls, l64, l85
                       in get_pion_lec_su3()]

    for k, v in qed_lecs.items():
        for i, sample in enumerate(v.resampled_params):
            fit_func_params[i][k] = sample

    avg_fit_func_params = {k: np.average([sample[k] for sample
                                          in fit_func_params])
                           for k in fit_func_params[0].keys()}

    def min_1_3(lec, targets):
        LS = lec['LS']

        def chi_sq(mu, md, ms):
            ff = fit_func(mu, md, ms, 2., -1., -1., **lec)
            c2 = sum((ff/targets - 1.0)**2)
            return c2
        m = minuit.Minuit(chi_sq, limit_mu=(0., 1e3), limit_md=(0., 1e3),
                          limit_ms=(0., 1e3))
        m.errors = dict(mu=1e-5, md=1e-5, ms=1e-5)
        m.values = dict(mu=2.606 / LS / 1000. / z_m,
                        md=4.50 / LS / 1000. / z_m,
                        ms=89.1 / LS / 1000. / z_m)
        m.printMode = 0
        m.maxcalls = 1000
        m.tol = 1e-7
        m.migrad()
        mu_fit = m.values["mu"]
        md_fit = m.values["md"]
        ms_fit = m.values["ms"]
        return mu_fit, md_fit, ms_fit

    ave_ls = avg_fit_func_params['LS']

    m_pi_plus = 139.57018/1000.  # M_pi+ in GeV
    m_k_zero = 497.614/1000.  # M_K0 in GeV
    m_k_plus = 493.667/1000.  # M_K+- in GeV

    m_pi_sq_lat = (m_pi_plus / ave_ls)**2
    m_k_plus_sq_lat = (m_k_plus / ave_ls)**2
    m_k_zero_sq_lat = (m_k_zero / ave_ls)**2

    targets = np.array([m_pi_sq_lat, m_k_plus_sq_lat, m_k_zero_sq_lat])

    mu, md, ms = min_1_3(avg_fit_func_params, targets)
    central_mu = mu * ave_ls * z_m
    central_md = md * ave_ls * z_m
    central_ms = ms * ave_ls * z_m

    log.debug("Ave: {}".format((central_mu * 1000., central_md * 1000.,
                               central_ms * 1000.)))
    jk_mu = []
    jk_md = []
    jk_ms = []

    for jk_lec in fit_func_params:
        LS = jk_lec['LS']
        m_pi_sq_lat = (m_pi_plus / LS)**2
        m_k_plus_sq_lat = (m_k_plus / LS)**2
        m_k_zero_sq_lat = (m_k_zero / LS)**2
        targets = np.array([m_pi_sq_lat, m_k_plus_sq_lat, m_k_zero_sq_lat])
        mu, md, ms = min_1_3(jk_lec, targets)
        jk_mu.append(mu * LS * z_m)
        jk_md.append(md * LS * z_m)
        jk_ms.append(ms * LS * z_m)

    resampler = Jackknife(n=1)
    mu_err = resampler.calculate_errors(central_mu, jk_mu)
    md_err = resampler.calculate_errors(central_md, jk_md)
    ms_err = resampler.calculate_errors(central_ms, jk_ms)
    to_return = {'mu': FitParams(central_mu, mu_err, jk_mu),
                 'md': FitParams(central_md, md_err, jk_md),
                 'ms': FitParams(central_ms, ms_err, jk_ms)}

    return to_return


measurements = [
    {
        'name': 'qed_lec_infv',
        'measurement': find_qed_lec,
        'template_name': 'su3/index.html',
    },
    {
        'name': 'mu_md_infv',
        'measurement': find_light_masses_su3,
        'template_name': 'su3/index.html',
    }
]
