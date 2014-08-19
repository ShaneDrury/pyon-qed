"""
Formulae for the mass-squared difference in SU(3)
"""
import numpy as np

from delmsq.lib.const import e_sq, pi_16


def del_m_sq_su3(x, C, Y2, Y3, Y4, Y5, deltamres, B0, F0, musq, L4, L5, mres):
    return np.array([del_m_sq_su3_one(xx, C, Y2, Y3, Y4, Y5, deltamres, B0, F0,
                                      musq, L4, L5, mres) for xx in x])


def del_m_sq_su3_one(x, C, Y2, Y3, Y4, Y5, deltamres, B0, F0, musq, L4, L5, mres):
    """
    Delta M-squared for SU(3).

    Ref: arXiv [1006.1311] eq. 11.4

    'line' variables refer to lines of the equation in the reference.
    """
    # (ml1, ml2, q1, q2, m_l)
    #m_1 = 0.010 # Mass of valence quark
    m_1 = x[0] + mres
    #m_3 = 0.010 # Mass of valence quark
    m_3 = x[1] + mres
    #m_4 = 0.005 # Mass of light sea quark

    # print(x[2])
    m_4 = x[4] + mres

    m_5 = m_4   # Take it to be degenerate
    m_6 = 0.040 + mres  # Mass of strange sea quark

    #q_1 = -1.0 / 3.0
    q_1 = x[2] / 3.0
    #q_3 = 0.0
    q_3 = x[3] / 3.0
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
    chi_1 = 2 * B0 * m_1
    chi_3 = 2 * B0 * m_3
    chi_1_3 = B0 * (m_1 + m_3)
    chi_1_4 = B0 * (m_1 + m_4)
    chi_1_5 = B0 * (m_1 + m_5)
    chi_1_6 = B0 * (m_1 + m_6)

    # chi_3_1 = B_0 * (m_3 + m_1)
    chi_3_4 = B0 * (m_3 + m_4)
    chi_3_5 = B0 * (m_3 + m_5)
    chi_3_6 = B0 * (m_3 + m_6)
    chi_bar_1 = 2 * B0 * (m_4 + m_5 + m_6) / 3.0

    line_1 = 2 * C * e_sq * q_1_3_sq / F0**2

    line_2 = - 48 * e_sq * C * L4 * q_1_3_sq * chi_bar_1 / F0**4 \
             - 16 * e_sq * C * L5 * q_1_3_sq * chi_1_3 / F0**4

    #line_3_a = -12 * e_sq * Y_1 * q_bar_sq * chi_1_3  # This term is zero
    line_3_a = 4 * e_sq * Y2 * (q_1 ** 2 * chi_1 + q_3 ** 2 * chi_3) \
        + 4 * e_sq * Y3 * q_1_3_sq * chi_1_3

    line_3_b = -4 * e_sq * Y4 * q_1 * q_3 * chi_1_3 \
        + 12 * e_sq * Y5 * q_1_3_sq * chi_bar_1

    line_3 = line_3_a + line_3_b

    line_4 = -2 * e_sq * C / F0**4 * pi_16 * q_1_3 \
        * (chi_1_4 * np.log(chi_1_4 / musq) * q_1_4 +
           chi_1_5 * np.log(chi_1_5 / musq) * q_1_5 +
           chi_1_6 * np.log(chi_1_6 / musq) * q_1_6)

    line_5 = 2 * e_sq * C / F0**4 * pi_16 * q_1_3 \
        * (chi_3_4 * np.log(chi_3_4 / musq) * q_3_4 +
           chi_3_5 * np.log(chi_3_5 / musq) * q_3_5 +
           chi_3_6 * np.log(chi_3_6 / musq) * q_3_6)

    line_6 = - q_1_3_sq * e_sq * pi_16 * chi_1_3 \
        * (3 * np.log(chi_1_3 / musq) - 4)

    line_7 = e_sq * deltamres * (q_1**2 + q_3**2)

    total = line_1 + line_2 + line_3 + line_4 + line_5 + line_6 + line_7
    return total


def find_pi_eta(chi_4, chi_5, chi_6):
    a = 2.0/3.0*(chi_4 + chi_5 + chi_6)
    b = 1.0/3.0*(chi_4*chi_5+chi_5*chi_6+chi_6*chi_4)
    chi_pi = (a-np.sqrt(a*a-4*b))/2.0
    chi_eta = a-chi_pi
    return chi_pi, chi_eta


def m_13_sq(mu, md, ms, qu, qd, qs, C=0, Y2=0, Y3=0, Y4=0, Y5=0, deltamres=0,
            mres=0, B0=0, F0=0, L64=0, L85=0, L4=0, L5=0, musq=0, LS=0):
    lecs = (C, Y2, Y3, Y4, Y5,
            deltamres, mres, B0, F0, L64, L85, L4, L5,
            musq)
    to_return = [
        m_13_sq_one(mu, md, mu, md, ms, qu, qd, *lecs),
        m_13_sq_one(mu, ms, mu, md, ms, qu, qs, *lecs),
        m_13_sq_one(md, ms, mu, md, ms, qd, qs, *lecs)
    ]
    return np.array(to_return)


def m_13_sq_one(m_1, m_3, m_4, m_5, m_6, q_1, q_3, C, Y2, Y3, Y4, Y5,
            deltamres, mres, B0, F0, L64, L85, L4, L5, musq):
    #q_1 = -1.0 / 3.0
    q_1 = q_1 / 3.0* np.sqrt(e_sq)
    #q_3 = 0.0
    q_3 = q_3 / 3.0* np.sqrt(e_sq)
    q_4 = +2. / 3. * np.sqrt(e_sq) # Quenched QED
    q_5 = -1. /3. * np.sqrt(e_sq)
    q_6 = -1. /3.  * np.sqrt(e_sq)

    q_1_3 = (q_1 - q_3)
    q_1_4 = (q_1 - q_4)
    q_1_5 = (q_1 - q_5)
    q_1_6 = (q_1 - q_6)
    q_3_1 = (q_3 - q_1)
    q_3_4 = (q_3 - q_4)
    q_3_5 = (q_3 - q_5)
    q_3_6 = (q_3 - q_6)
    q_1_3_sq = q_1_3**2
    q_3_1_sq = q_3_1**2
    q_bar_sq = (q_4**2 + q_5**2 + q_6**2)/3.0
    chi_1 = 2 * B0 * m_1
    chi_3 = 2 * B0 * m_3
    chi_4 = 2 * B0 * m_4
    chi_5 = 2 * B0 * m_5
    chi_6 = 2 * B0 * m_6
    chi_1_3 = B0 * (m_1 + m_3)
    chi_1_4 = B0 * (m_1 + m_4)
    chi_1_5 = B0 * (m_1 + m_5)
    chi_1_6 = B0 * (m_1 + m_6)

    chi_3_1 = B0 * (m_3 + m_1)
    chi_3_4 = B0 * (m_3 + m_4)
    chi_3_5 = B0 * (m_3 + m_5)
    chi_3_6 = B0 * (m_3 + m_6)
    chi_bar_1 = 2 * B0 * ( m_4 + m_5 + m_6 ) / 3.0
    chi_pi, chi_eta = find_pi_eta(chi_4, chi_5, chi_6)

    def R_456(i,j,k,l):
        return ((i - chi_4) * (i - chi_5) * (i - chi_6)) / (i - j) / (i - k) / (i - l)

    R_pi_eta_1_3 = R_456(chi_pi, chi_eta, chi_1, chi_3)
    R_eta_pi_1_3 = R_456(chi_eta, chi_pi, chi_1, chi_3)
    #R_1_3_pi_eta = R_456(chi_1, chi_3, chi_pi, chi_eta)
    #R_3_1_pi_eta = R_456(chi_3, chi_1, chi_pi, chi_eta)

    total = chi_1_3
    total += L64 / F0**2 * chi_1_3 * chi_bar_1
    total += L85 / F0**2 * chi_1_3 ** 2
    total += pi_16 / (3. * F0**2) * chi_1_3 * (R_pi_eta_1_3 * chi_pi * np.log(chi_pi / musq))
    total += pi_16 / (3. * F0**2) * chi_1_3 * (R_eta_pi_1_3 * chi_eta * np.log(chi_eta / musq))
    total += 2. * C / F0**2 * q_1_3_sq
    total += -48.  * C / F0**4 * L4 * q_1_3_sq * chi_bar_1
    total += -16. *  C / F0**4 * L5 * q_1_3_sq * chi_1_3
    total +=  4 * Y2 * (q_1*q_1 * chi_1 + q_3 * q_3 *chi_3) # m2=m2+Y2*4.0*(q1*q1*chi1+q3*q3*chi3);
    total +=  Y3 * 4.0 * (q_1_3_sq * chi_1_3)  #     m2=m2+Y3*4.0*(q13*q13*chi13);
    total += - Y4 * 4.0 * (q_1 * q_3 * chi_1_3)  #     m2=m2-Y4*4.0*(q1*q3*chi13);
    total += 12 *  Y5 * q_1_3_sq * chi_bar_1 #     m2=m2+Y5*12.0*(q13*q13*chi1bar);
    #total += - q_1_3**2 *  pi_16 * chi_1_3 * (3. * np.log(chi_1_3 / mu_sq) - 4.)
    #m2=m2+(-pi16)*chi13*log(chi13/miu/miu)*q13*q13; // Same
    #m2=m2+4.0*pi16*(1.0-log(chi13/miu/miu))*q13*q13*chi13; // Same                                                                                      #m2=m2-4.0*(-pi16)/2.0*log(chi13/miu/miu)*q13*q13*chi13;
    total += -pi_16 * chi_1_3 * np.log(chi_1_3 / musq) * q_1_3_sq
    total += 4.0 * pi_16 * (1.0 - np.log(chi_1_3 / musq)) * q_1_3_sq * chi_1_3
    total += 4.0 * pi_16 / 2.0 * np.log(chi_1_3 / musq) * q_1_3_sq * chi_1_3
    total += -2 *  C / F0**4 * pi_16 * q_1_3 * chi_1_4 * np.log(chi_1_4 / musq) * q_1_4
    total +=  -2 *  C / F0**4 * pi_16 * q_1_3 *chi_1_5 * np.log(chi_1_5 / musq) * q_1_5
    total += 2 *  C / F0**4 * pi_16 * q_1_3 * chi_3_4 * np.log(chi_3_4 / musq) * q_3_4
    total += 2 *  C / F0**4 * pi_16 * q_1_3 * chi_3_5 * np.log(chi_3_5 / musq) * q_3_5
    total += -2 *  C / F0**4 * pi_16 * q_1_3 * chi_1_6 * np.log(chi_1_6 / musq) * q_1_6
    total += 2 *  C / F0**4 * pi_16 * q_1_3 * chi_3_6 * np.log(chi_3_6 / musq) * q_3_6
    #line_10_b = pi_16 / (3. * F_0**2) * chi_1_3 * (R_1_3_pi_eta * chi_1 * np.log(chi_1 / mu_sq) + R_3_1_pi_eta * chi_3 * np.log(chi_3 / mu_sq))
    #total +=  delta_m_res * (q_1**2 + q_3**2)
    return total