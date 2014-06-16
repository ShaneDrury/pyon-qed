"""
Formulae for the mass-squared difference in SU(3)
"""
import numpy as np

from delmsq.lib.const import e_sq, pi_16


def del_m_sq_su3(x, C, Y_2, Y_3, Y_4, Y_5, delta_m_res, B_0, F_0, mu_sq, L_4,
                 L_5, mres):
    """
    Delta M-squared for SU(3).

    Ref: arXiv [1006.1311] eq. 11.4

    'line' variables refer to lines of the equation in the reference.

    :param x:
    :param C:
    :param Y_2:
    :param Y_3:
    :param Y_4:
    :param Y_5:
    :param delta_m_res:
    :param B_0:
    :param F_0:
    :param mu_sq:
    :param L_4:
    :param L_5:
    :param mres:
    :return:
    """
    #m_1 = 0.010 # Mass of valence quark
    m_1 = x[0] + mres
    #m_3 = 0.010 # Mass of valence quark
    m_3 = x[1] + mres
    #m_4 = 0.005 # Mass of light sea quark
    m_4 = x[2] + mres

    m_5 = m_4   # Take it to be degenerate
    m_6 = 0.040 + mres  # Mass of strange sea quark

    #q_1 = -1.0 / 3.0
    q_1 = x[3] / 3.0
    #q_3 = 0.0
    q_3 = x[4] / 3.0
    q_4 = 0.0  # Quenched QED
    q_5 = 0.0
    q_6 = 0.0

    q_1_3 = (q_1 - q_3)
    q_1_4 = (q_1 - q_4)
    q_1_5 = (q_1 - q_5)
    q_1_6 = (q_1 - q_6)
    # q_3_1 = (q_3 - q_1)
    q_3_4 = (q_3 - q_4)
    q_3_5 = (q_3 - q_5)
    q_3_6 = (q_3 - q_6)

    q_1_3_sq = q_1_3**2
    # q_3_1_sq = q_3_1**2  # unused
    # q_bar_sq = (q_4**2 + q_5**2 + q_6**2)/3.0  # zero
    chi_1 = 2 * B_0 * m_1
    chi_3 = 2 * B_0 * m_3
    chi_1_3 = B_0 * (m_1 + m_3)
    chi_1_4 = B_0 * (m_1 + m_4)
    chi_1_5 = B_0 * (m_1 + m_5)
    chi_1_6 = B_0 * (m_1 + m_6)

    # chi_3_1 = B_0 * (m_3 + m_1)
    chi_3_4 = B_0 * (m_3 + m_4)
    chi_3_5 = B_0 * (m_3 + m_5)
    chi_3_6 = B_0 * (m_3 + m_6)
    chi_bar_1 = 2 * B_0 * (m_4 + m_5 + m_6) / 3.0

    line_1 = 2 * C * e_sq * q_1_3_sq / F_0**2

    line_2 = - 48 * e_sq * C * L_4 * q_1_3_sq * chi_bar_1 / F_0**4 \
             - 16 * e_sq * C * L_5 * q_1_3_sq * chi_1_3 / F_0**4

    #line_3_a = -12 * e_sq * Y_1 * q_bar_sq * chi_1_3  # This term is zero
    line_3_a = 4 * e_sq * Y_2 * (q_1 ** 2 * chi_1 + q_3 ** 2 * chi_3) \
        + 4 * e_sq * Y_3 * q_1_3_sq * chi_1_3

    line_3_b = -4 * e_sq * Y_4 * q_1 * q_3 * chi_1_3 \
        + 12 * e_sq * Y_5 * q_1_3_sq * chi_bar_1

    line_3 = line_3_a + line_3_b

    line_4 = -2 * e_sq * C / F_0**4 * pi_16 * q_1_3 \
        * (chi_1_4 * np.log(chi_1_4 / mu_sq) * q_1_4 +
           chi_1_5 * np.log(chi_1_5 / mu_sq) * q_1_5 +
           chi_1_6 * np.log(chi_1_6 / mu_sq) * q_1_6)

    line_5 = 2 * e_sq * C / F_0**4 * pi_16 * q_1_3 \
        * (chi_3_4 * np.log(chi_3_4 / mu_sq) * q_3_4 +
           chi_3_5 * np.log(chi_3_5 / mu_sq) * q_3_5 +
           chi_3_6 * np.log(chi_3_6 / mu_sq) * q_3_6)

    line_6 = - q_1_3_sq * e_sq * pi_16 * chi_1_3 \
        * (3 * np.log(chi_1_3 / mu_sq) - 4)

    line_7 = e_sq * delta_m_res * (q_1**2 + q_3**2)

    total = line_1 + line_2 + line_3 + line_4 + line_5 + line_6 + line_7
    return total