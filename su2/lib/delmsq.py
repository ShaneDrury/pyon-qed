import numpy as np

from delmsq.lib.const import e_sq, pi_16



# def del_m_sq_su2_fv(x, C, Y2, Y3, Y4, Y5, correction, deltamres, B0, F0, musq,
#                     L4, L5, mres):
#     return np.array([del_m_sq_su2_fv_one(xx, C, Y2, Y3, Y4, Y5, deltamres, B0,
#                                          F0, musq, L4, L5, mres, cc)
#                      for xx, cc in zip(x, correction)])

def del_m_sq_su2_fv_one(x, C, Y_2, Y_3, Y_4, Y_5, delta_m_res, B_0, F_0, mu_sq,
                        L_4, L_5, mres, correction):

    #m_1 = 0.010 # Mass of valence quark
    m_1 = x[0] + mres
    #m_3 = 0.010 # Mass of valence quark
    m_3 = x[1] + mres
    #m_4 = 0.005 # Mass of light sea quark
    m_4 = x[4] + mres

    m_5 = m_4   # Take it to be degenerate
    # m_6 = 0.040 + mres  # Mass of strange sea quark

    #q_1 = -1.0 / 3.0
    q_1 = x[2] / 3.0 * np.sqrt(e_sq)
    #q_3 = 0.0
    q_3 = x[3] / 3.0 * np.sqrt(e_sq)
    q_4 = 0.0  # Quenched QED
    q_5 = 0.0
    # q_6 = 0.0

    q_1_3 = (q_1 - q_3)
    q_1_4 = (q_1 - q_4)
    q_1_5 = (q_1 - q_5)
    # q_1_6 = (q_1 - q_6)
    # q_3_1 = (q_3 - q_1)
    q_3_4 = (q_3 - q_4)
    q_3_5 = (q_3 - q_5)
    # q_3_6 = (q_3 - q_6)

    q_1_3_sq = q_1_3**2
    # q_3_1_sq = q_3_1**2
    # q_bar_sq = (q_4**2 + q_5**2 + q_6**2)/3.0
    chi_1 = 2 * B_0 * m_1
    chi_3 = 2 * B_0 * m_3
    chi_4 = 2 * B_0 * m_4
    chi_5 = 2 * B_0 * m_5
    chi_1_3 = B_0 * (m_1 + m_3)
    chi_1_4 = B_0 * (m_1 + m_4)
    chi_1_5 = B_0 * (m_1 + m_5)
    # chi_1_6 = B_0 * (m_1 + m_6)

    # chi_3_1 = B_0 * (m_3 + m_1)
    chi_3_4 = B_0 * (m_3 + m_4)
    chi_3_5 = B_0 * (m_3 + m_5)
    # chi_3_6 = B_0 * (m_3 + m_6)

    # chi_bar_1 = 2 * B_0 * (m_4 + m_5 + m_6) / 3.0

    def J(chi):
        return pi_16 * (np.log(chi/mu_sq) - 1.)

    def K(chi):
        return -0.5 * pi_16 * chi * np.log(chi / mu_sq)

    def I_1(chi):
        return pi_16 * chi * np.log(chi / mu_sq)

    # LOQED
    lo_qed = 2 * C * q_1_3_sq / F_0**2

    # NLOQED
    line_1 = C / F_0**4 * (-48. * L_4 * q_1_3_sq * (chi_4 + chi_5) / 3.0 - 16. * L_5 * q_1_3_sq * chi_1_3)
    line_2 = -q_1_3_sq * (4. * chi_1_3 * J(chi_1_3) + 2. * K(chi_1_3))
    line_3 = -2. * C / F_0**4 * (I_1(chi_1_4) * q_1_4 * q_1_3 - I_1(chi_3_4) * q_3_4 * q_1_3
                                 + I_1(chi_1_5) * q_1_5 * q_1_3 - I_1(chi_3_5) * q_3_5 * q_1_3)
    line_4 = Y_2 * 4. * (q_1**2 * chi_1 + q_3**2 * chi_3) + Y_3 * 4. * q_1_3_sq * chi_1_3
    line_5 = -Y_4 * 4. * q_1 * q_3 * chi_1_3 + Y_5 * 4. * q_1_3_sq * (chi_4 + chi_5)
    nlo_qed = line_1 + line_2 + line_3 + line_4 + line_5
    # LAT
    lat = delta_m_res * (q_1**2 + q_3**2)
    total = lo_qed + nlo_qed + lat - correction * C / F_0**4
    return total