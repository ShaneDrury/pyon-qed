import logging

import numpy as np

from delmsq.lib.const import e_sq


log = logging.getLogger(__name__)


def coefficients(x, mres, B_0, F_0, mu_sq, correction):
    m_1 = x[0] + mres
    m_3 = x[1] + mres
    m_4 = x[4] + mres
    m_5 = m_4   # Take it to be degenerate
    # m_6 = 0.040 + mres # Mass of strange sea quark
    q_1 = x[2] / 3.0 * np.sqrt(e_sq)
    q_3 = x[3] / 3.0 * np.sqrt(e_sq)
    if m_3 < m_1:
        m_1, m_3 = m_3, m_1
        q_1, q_3 = q_3, q_1

    chi_1_4 = B_0 * (m_1 + m_4)
    # chi_1_5 = B_0 * (m_1 + m_5)
    sum_log = 1.0/(4*3.1415926)/(4*3.1415926)/F_0/F_0*2.0*chi_1_4 * \
              np.log(chi_1_4/mu_sq)

    A_11 = q_1**2 * (2.0 - sum_log - correction / F_0**2)
    A_21 = q_1**2 * (2.0 - 3.0 * sum_log - 3.0 * correction / F_0**2)
    A_s11 = q_3**2
    A_s2 = q_1 * q_3 * (2.0 - sum_log - correction / F_0**2)

    x_3 = m_1 * (q_1 + q_3)**2
    x_4 = m_1 * (q_1 - q_3)**2
    x_5 = m_1 * (q_1**2 - q_3**2)
    x_6 = 0.5 * (m_4 + m_5) * (q_1 + q_3)**2
    x_7 = 0.5 * (m_4 + m_5) * (q_1 - q_3)**2
    x_8 = 0.5 * (m_4 + m_5) * (q_1**2 - q_3**2)

    # print(x)
    # print(np.array([A_11, A_21, A_s11, A_s2, x_3, x_4, x_5, x_6, x_7, x_8]))
    # exit()
    return np.array([A_11, A_21, A_s11, A_s2, x_3, x_4, x_5, x_6, x_7, x_8])


def get_y(x, ave, dmres, correction):
    q_1 = x[2] / 3.0 * np.sqrt(e_sq)
    q_3 = x[3] / 3.0 * np.sqrt(e_sq)
    y = ave - dmres * (q_1**2 + q_3**2) \
        + correction * (q_1 - q_3) * (q_1 - q_3)
    return y


def filter_kaon_del_m_sq(all_del_m_sq, m_3):
    filtered_delmsq = {}
    for m_l, v in all_del_m_sq.items():
        if m_l not in (0.005, 0.01):
            continue
        results = v()
        for k, delmsq in results.items():
            ml1, ml2, q1, q2 = k
            new_key = (ml1, ml2, q1, q2, m_l)
            # if ml2 < ml1:
            #     ml1, ml2 = ml2, ml1
            #     q1, q2 = q2, q1
            if check_masses_kaon(ml1, ml2, m_3):
                log.debug("Accepting ml={} {}, {}".format(m_l, (ml1, ml2),
                                                          (q1, q2)))
                filtered_delmsq[new_key] = delmsq
    return filtered_delmsq


def check_masses_kaon(m1, m2, m_3) -> bool:
    if m2 < m1:
        return _check_masses_symm(m2, m1, m_3)
    if m1 < m2:
        return _check_masses_symm(m1, m2, m_3)


def _check_masses_symm(m1, m2, m_3) -> bool:
    if m1 not in (0.005, 0.01):
        return False
    if m2 != m_3:
        return False
    return True