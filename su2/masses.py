import minuit
import logging

from pyon.lib.fitting.base import FitParams
from pyon.lib.resampling import Jackknife
import numpy as np

from delmsq.lib.const import pi_16, e_sq
from su2.lec import get_pion_lec_su2, get_qed_lec_pion_fv, \
    get_qed_lec_kaon_fv_002, get_qed_lec_kaon_fv_003
from su2.models import KaonLECSU2


log = logging.getLogger(__name__)


def pion_m_sq(m_1, m_3, m_4, m_5, m_6, q_1, q_3, B_0, F_0, L_2_6_L_4,
              L_2_8_L_5, L_4, L_5, mres, mu_sq, C, Y_2, Y_3, Y_4, Y_5,
              deltamres):
    # Order of arguments is (mass, charge, Pion QCD LECs, Pion QED LECs)

    q_1 = q_1 / 3.0 * np.sqrt(e_sq)
    q_3 = q_3 / 3.0 * np.sqrt(e_sq)
    q_4 = +2. / 3. * np.sqrt(e_sq)
    q_5 = -1. / 3. * np.sqrt(e_sq)
    # q_6 = -1. /3.  * np.sqrt(e_sq)

    q_1_3 = (q_1 - q_3)
    q_1_4 = (q_1 - q_4)
    q_1_5 = (q_1 - q_5)
    # q_1_6 = (q_1 - q_6)
    # q_3_1 = (q_3 - q_1)
    q_3_4 = (q_3 - q_4)
    q_3_5 = (q_3 - q_5)
    # q_3_6 = (q_3 - q_6)
    # q_1_3_sq = q_1_3**2
    # q_3_1_sq = q_3_1**2
    # q_bar_sq = (q_4**2 + q_5**2 + q_6**2)/3.0
    chi_1 = 2 * B_0 * m_1
    chi_3 = 2 * B_0 * m_3
    chi_4 = 2 * B_0 * m_4
    chi_5 = 2 * B_0 * m_5
    # chi_6 = 2 * B_0 * m_6
    chi_1_3 = B_0 * (m_1 + m_3)
    chi_1_4 = B_0 * (m_1 + m_4)
    chi_1_5 = B_0 * (m_1 + m_5)


    # chi_3_1 = B_0 * (m_3 + m_1)
    chi_3_4 = B_0 * (m_3 + m_4)
    chi_3_5 = B_0 * (m_3 + m_5)

    chi_bar_1 = (chi_4 + chi_5) / 3.0
    # chi_1_6=(chi_1+chi_6)/2.0
    # chi_3_6=(chi_3+chi_6)/2.0

    m2 = chi_1_3  # Taken from Ran's C Code
    m2 += L_2_6_L_4 * chi_bar_1 * chi_1_3 / F_0 / F_0
    m2 += L_2_8_L_5 * chi_1_3 * chi_1_3 / F_0 / F_0
    R = (-3.0 / 4.0) * pi_16 * (chi_4 + chi_5) * np.log(
        (chi_4 + chi_5) / 2.0 / mu_sq)
    m2 -= 1.0 / 3.0 * chi_1_3 * R / F_0 / F_0

    m2 += 2.0 * C * q_1_3 * q_1_3 / F_0 / F_0
    m2 -= C * 48.0 / F_0 / F_0 / F_0 / F_0 * L_4 * q_1_3 * q_1_3 * chi_bar_1
    m2 -= C * 16.0 / F_0 / F_0 / F_0 / F_0 * L_5 * q_1_3 * q_1_3 * chi_1_3

    m2 += Y_2 * 4.0 * (q_1 * q_1 * chi_1 + q_3 * q_3 * chi_3)
    m2 += Y_3 * 4.0 * (q_1_3 * q_1_3 * chi_1_3)
    m2 -= Y_4 * 4.0 * (q_1 * q_3 * chi_1_3)
    m2 += Y_5 * 12.0 * (q_1_3 * q_1_3 * chi_bar_1)
    m2 += (-pi_16) * chi_1_3 * np.log(chi_1_3 / mu_sq) * q_1_3 * q_1_3
    m2 += 4.0 * pi_16 * (
        1.0 - np.log(chi_1_3 / mu_sq)) * q_1_3 * q_1_3 * chi_1_3
    m2 -= 4.0 * (-pi_16) / 2.0 * np.log(
        chi_1_3 / mu_sq) * q_1_3 * q_1_3 * chi_1_3
    m2 += C * 2.0 / F_0 / F_0 / F_0 / F_0 * (-pi_16) * chi_1_4 * np.log(
        chi_1_4 / mu_sq) * q_1_4 * q_1_3
    m2 += C * 2.0 / F_0 / F_0 / F_0 / F_0 * (-pi_16) * chi_1_5 * np.log(
        chi_1_5 / mu_sq) * q_1_5 * q_1_3
    m2 -= C * 2.0 / F_0 / F_0 / F_0 / F_0 * (-pi_16) * chi_3_4 * np.log(
        chi_3_4 / mu_sq) * q_3_4 * q_1_3
    m2 -= C * 2.0 / F_0 / F_0 / F_0 / F_0 * (-pi_16) * chi_3_5 * np.log(
        chi_3_5 / mu_sq) * q_3_5 * q_1_3
    return m2


def find_pi_eta(chi_4, chi_5, chi_6):
    a = 2.0 / 3.0 * (chi_4 + chi_5 + chi_6)
    b = 1.0 / 3.0 * (chi_4 * chi_5 + chi_5 * chi_6 + chi_6 * chi_4)
    chi_pi = (a - np.sqrt(a * a - 4 * b)) / 2.0
    chi_eta = a - chi_pi
    return chi_pi, chi_eta


def k_m_sq(m_1, m_3, m_4, m_5, m_6, q_1, q_3, B_0, F_0, L_2_6_L_4, L_2_8_L_5,
           L_4, L_5, mres, mu_sq, C, Y_2, Y_3, Y_4, Y_5, deltamres, M2, A_3,
           A_4, A_11, A_21, A_s11, A_s2, x_3, x_4, x_5, x_6, x_7, x_8):
    # Order of arguments is (mass, charge, Pion QCD LECs, Pion QED LECs, Kaon QCD LECs, Kaon QED LECs)
    # Note M is actually M**2, so no need to square it in formula
    q_1 = q_1 / 3.0 * np.sqrt(e_sq)
    q_3 = q_3 / 3.0 * np.sqrt(e_sq)
    q_4 = +2. / 3. * np.sqrt(e_sq)
    q_5 = -1. / 3. * np.sqrt(e_sq)
    # q_6 = -1. /3.  * np.sqrt(e_sq)
    chi_1_4 = B_0 * (m_1 + m_4)
    chi_1_5 = B_0 * (m_1 + m_5)

    total = M2 - 4. * B_0 * (A_3 * m_1 + A_4 * (m_4 + m_5))
    total += 2. * (
        A_11 + A_21) * q_1 ** 2 + A_s11 * q_3 ** 2 + 2. * A_s2 * q_1 * q_3
    total += m_1 * (x_3 * (q_1 + q_3) ** 2 + x_4 * (q_1 - q_3) ** 2 + x_5 * (
        q_1 ** 2 - q_3 ** 2))
    total += 0.5 * (m_4 + m_5) * (
        x_6 * (q_1 + q_3) ** 2 + x_7 * (q_1 - q_3) ** 2 + x_8 * (
            q_1 ** 2 - q_3 ** 2))

    logs = -pi_16 / F_0 ** 2 * A_11 * (
        (q_1 * q_1 - q_4 * q_4) * chi_1_4 * np.log(chi_1_4 / mu_sq) + (
            q_1 * q_1 - q_5 * q_5) * chi_1_5 * np.log(chi_1_5 / mu_sq));
    logs -= pi_16 / F_0 ** 2 * A_21 * (
        2.0 * q_1 * q_1 - 2.0 * q_1 * q_4 + (q_1 - q_4) * (
            q_1 - q_4)) * chi_1_4 * np.log(chi_1_4 / mu_sq)
    logs -= pi_16 / F_0 ** 2 * A_21 * (
        2.0 * q_1 * q_1 - 2.0 * q_1 * q_5 + (q_1 - q_5) * (
            q_1 - q_5)) * chi_1_5 * np.log(chi_1_5 / mu_sq)
    logs -= pi_16 / F_0 ** 2 * A_s2 * q_3 * (q_1 - q_4) * chi_1_4 * np.log(
        chi_1_4 / mu_sq)
    logs -= pi_16 / F_0 ** 2 * A_s2 * q_3 * (q_1 - q_5) * chi_1_5 * np.log(
        chi_1_5 / mu_sq)
    total += logs
    # total += delta_m_res * (q_1**2 + q_3**2)
    return total


def k_m_sq_fix_ms(m_1, m_3, m_4, m_5, m_6, q_1, q_3, mres, all_lecs_l,
                  all_lecs_h):
    mk_l = k_m_sq(m_1, 0.02, m_4, m_5, m_6, q_1, q_3, **all_lecs_l)
    mk_h = k_m_sq(m_1, 0.03, m_4, m_5, m_6, q_1, q_3, **all_lecs_h)
    # Extrapolate linearly
    mass_2 = (mk_h - mk_l) / 0.01 * (m_3 - 0.02 - mres) + mk_l
    return mass_2


def min_m_1_3(target_pion_plus, target_kaon_plus, target_kaon_zero, qu, qd, qs,
              pion_qcd_lecs, pion_qed_lecs, kaon_qcd_lecs, kaon_qed_lecs, LS):
    # Build lec blocks
    all_pion_lecs = {}
    all_pion_lecs.update(pion_qcd_lecs)
    all_pion_lecs.update(pion_qed_lecs)
    all_lecs_l = {}
    all_lecs_h = {}
    all_lecs_l.update(all_pion_lecs)
    all_lecs_l.update(kaon_qcd_lecs[0])
    all_lecs_l.update(kaon_qed_lecs[0])
    all_lecs_h.update(all_pion_lecs)
    all_lecs_h.update(kaon_qcd_lecs[1])
    all_lecs_h.update(kaon_qed_lecs[1])

    mres = all_pion_lecs['mres']  # Used in the extrapolation of ms
    # m_u = 2.09 / LS / 1000. / 1.5458
    # m_d = 4.5 / LS / 1000. / 1.5458
    # m_s = 95. / LS / 1000. / 1.5458

    def chi_sq(mu, md, ms):
        chi2 = (pion_m_sq(mu, md, mu, md, ms, qu, qd,
                          **all_pion_lecs) / target_pion_plus - 1.0) ** 2  # Pion
        chi2 += (k_m_sq_fix_ms(mu, ms, mu, md, ms, qu, qs, mres, all_lecs_l,
                               all_lecs_h) / target_kaon_plus - 1.0) ** 2  # K+-
        chi2 += (k_m_sq_fix_ms(md, ms, mu, md, ms, qd, qs, mres, all_lecs_l,
                               all_lecs_h) / target_kaon_zero - 1.0) ** 2  # K0
        return chi2

    m = minuit.Minuit(chi_sq, limit_mu=(0., 1e3), limit_md=(0., 1e3),
                      limit_ms=(0., 1e3))
    m.errors = dict(mu=1e-5, md=1e-5, ms=1e-5)
    m.values = dict(mu=2.0 / LS / 1000., md=4.0 / LS / 1000.,
                    ms=105. / LS / 1000.)
    m.printMode = 0
    m.maxcalls = 1000
    m.tol = 1e-6
    m.migrad()
    mu_fit = m.values["mu"]
    md_fit = m.values["md"]
    ms_fit = m.values["ms"]
    return mu_fit, md_fit, ms_fit


def get_kaon_lec_02():
    return get_kaon_lec_su2(0.02)


def get_kaon_lec_03():
    return get_kaon_lec_su2(0.03)


def get_kaon_lec_su2(m_s):
    all_lec = KaonLECSU2.objects.filter(m_s=m_s).order_by('config_number')
    jk_M2 = [qs.M2 for qs in all_lec]
    jk_A3 = [qs.A_3 for qs in all_lec]
    jk_A4 = [qs.A_4 for qs in all_lec]
    return zip(jk_M2, jk_A3, jk_A4)


def avg_list_dict(lst):
    return {k: np.average([sample[k] for sample in lst])
            for k in lst[0].keys()}


def dict_fitparams_to_list_dicts(d) -> list:
    # dict of FitParams -> list of dicts
    rp = {k: v.resampled_params for k, v in d.items()}
    to_return = [None] * len(list(rp.values())[0])
    for i, el in enumerate(to_return):
        to_return[i] = {}
    for k, v in rp.items():
        for i, jk in enumerate(v):
            to_return[i][k] = jk
    return to_return


def get_su2_masses():
    pion_qcd_lecs = [dict(B_0=b0,
                          F_0=f0,
                          mu_sq=musq,
                          L_4=l4,
                          L_5=l5,
                          mres=mmres,
                          ls=ls,
                          L_2_6_L_4=l64,
                          L_2_8_L_5=l85)
                     for b0, f0, musq, l4, l5, mmres, ls, l64, l85 in
                     get_pion_lec_su2()]

    pion_qed_lecs_dict = get_qed_lec_pion_fv()
    pion_qed_lecs = dict_fitparams_to_list_dicts(pion_qed_lecs_dict)
    kaon_qcd_lec_002 = [dict(M2=M2,
                             A_3=A3,
                             A_4=A4) for M2, A3, A4 in get_kaon_lec_02()]
    kaon_qcd_lec_003 = [dict(M2=M2,
                             A_3=A3,
                             A_4=A4) for M2, A3, A4 in get_kaon_lec_03()]


    kaon_qed_lec_002_dict = get_qed_lec_kaon_fv_002()
    kaon_qed_lec_003_dict = get_qed_lec_kaon_fv_003()
    kaon_qed_lec_002 = dict_fitparams_to_list_dicts(kaon_qed_lec_002_dict)
    kaon_qed_lec_003 = dict_fitparams_to_list_dicts(kaon_qed_lec_003_dict)
    avg_kaon_qed_lecs_002 = {k: v.average_params
                             for k, v in kaon_qed_lec_002_dict.items()}
    avg_kaon_qed_lecs_003 = {k: v.average_params
                             for k, v in kaon_qed_lec_003_dict.items()}

    kaon_qed_lecs = [(k2, k3) for k2, k3 in zip(kaon_qed_lec_002, kaon_qed_lec_003)]

    avg_kaon_qed_lecs = [avg_kaon_qed_lecs_002, avg_kaon_qed_lecs_003]

    avg_pion_qcd_lecs = avg_list_dict(pion_qcd_lecs)
    avg_pion_qed_lecs = {k: v.average_params for k, v in pion_qed_lecs_dict.items()}
    avg_kaon_qcd_lecs_002 = avg_list_dict(kaon_qcd_lec_002)
    avg_kaon_qcd_lecs_003 = avg_list_dict(kaon_qcd_lec_003)

    kaon_qcd_lecs = [(k2, k3) for k2, k3 in zip(kaon_qcd_lec_002, kaon_qcd_lec_003)]
    avg_kaon_qcd_lecs = [avg_kaon_qcd_lecs_002, avg_kaon_qcd_lecs_003]

    jk_LS = [d['ls'] for d in pion_qcd_lecs]
    for d in pion_qcd_lecs:
        d.pop('ls')
    ave_LS = avg_pion_qcd_lecs.pop('ls')

    m_pi_plus = 139.57018/1000.  # M_pi+ in GeV
    m_k_plus = 493.677/1000.  # M_K+- in GeV
    m_k_zero = 497.614/1000.  # M_K0 in GeV

    z_m = 1.5458  # Renormalization constant
    m_pi_sq_lat = (m_pi_plus / ave_LS)**2
    m_k_plus_sq_lat = (m_k_plus / ave_LS)**2
    m_k_zero_sq_lat = (m_k_zero / ave_LS)**2

    #print "Average"
    m_u, m_d, m_s = min_m_1_3(m_pi_sq_lat, m_k_plus_sq_lat, m_k_zero_sq_lat,
                              2., -1., -1.,
                              avg_pion_qcd_lecs,
                              avg_pion_qed_lecs,
                              avg_kaon_qcd_lecs,
                              avg_kaon_qed_lecs, ave_LS)

    central_mu = m_u * ave_LS * z_m
    central_md = m_d * ave_LS * z_m
    central_ms = m_s * ave_LS * z_m
    print(central_mu, central_md, central_ms)

    jk_mu = []
    jk_md = []
    jk_ms = []
    #print "Jackknife"
    # kaon_qcd_lecs = np.swapaxes(kaon_qcd_lecs, 0, 1)
    # kaon_qed_lecs = np.swapaxes(kaon_qed_lecs, 0, 1)
    i = 0
    for pion_qcd_lec, pion_qed_lec, kaon_qcd_lec, kaon_qed_lec, LS in \
            zip(pion_qcd_lecs, pion_qed_lecs, kaon_qcd_lecs, kaon_qed_lecs,
                jk_LS):

        # print(kaon_qed_lec)
        # exit()
        m_pi_sq_lat = (m_pi_plus / LS)**2
        m_k_plus_sq_lat = (m_k_plus / LS)**2
        m_k_zero_sq_lat = (m_k_zero / LS)**2
        m_u, m_d, m_s = min_m_1_3(m_pi_sq_lat, m_k_plus_sq_lat,
                                  m_k_zero_sq_lat, 2., -1., -1.,
                                  pion_qcd_lec,
                                  pion_qed_lec,
                                  kaon_qcd_lec,
                                  kaon_qed_lec, LS)
        jk_mu.append(m_u * LS * z_m)
        jk_md.append(m_d * LS * z_m)
        jk_ms.append(m_s * LS * z_m)
        i += 1
        log.debug(i)

    resampler = Jackknife(n=1)
    mu_err = resampler.calculate_errors(central_mu, jk_mu)
    md_err = resampler.calculate_errors(central_md, jk_md)
    ms_err = resampler.calculate_errors(central_ms, jk_ms)
    log.debug((np.average(jk_mu) * 1000., mu_err * 1000.,
               np.average(jk_md) * 1000., md_err * 1000.,
               np.average(jk_ms) * 1000., ms_err * 1000.))
    to_return = {
        'mu': FitParams(central_mu, mu_err, jk_mu),
        'md': FitParams(central_md, md_err, jk_md),
        'ms': FitParams(central_ms, ms_err, jk_ms),
    }
    return to_return