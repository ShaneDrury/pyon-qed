"""
Finite Volume
"""
import logging
from subprocess import Popen, PIPE

from pyon.core.cache import cache_data

from meas24c.measurements import covariant_delmsq_meas
from su2.lib.kaon import filter_kaon_del_m_sq
from su2.models import PionLECSU2
from su3.lib.statistics import pad
from su3.views import filter_del_m_sq


log = logging.getLogger(__name__)


def mathematica_float(out):
    # Converts Mathematica's weird scientific notation into a float
    headtail = out.split("*^")
    if len(headtail) > 1:
        fl = float(headtail[0]) * 10**(int(headtail[1][:-1]))
    else:
        fl = float(out)
    return fl


def get_fvc(*args):
    #Build command
    # cmd = "/home/srd1g10/Google Drive/pycharmProjects/pyon-qed/su2/lib/external/prop_to_c_correction_su2.m"
    cmd = "/home/srd1g10/Dropbox/Projects/EM/Scripts/24c/all/fv/prop_to_c_correction_su2.m"
    pp = [cmd]
    for arg in args:
        pp.append(str(arg))
    p = Popen(pp, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    stdout = stdout.decode('ascii')
    vals = stdout.split('\n')[:4]
    PIFVC = mathematica_float(vals[0] + '\n')
    PIFV = mathematica_float(vals[1] + '\n')
    KFVC = mathematica_float(vals[2] + '\n')
    KFV = mathematica_float(vals[3] + '\n')
    log.debug("{}".format((PIFV, PIFVC, KFVC, KFV)))
    return PIFV, PIFVC, KFVC, KFV


def get_pion_lec_su2_fv():
    """
    QCD Pion LECs for SU2 finite vol corrections (Don't need all of them)
    """
    all_lec = PionLECSU2.objects.order_by('config_number')
    jk_b0 = [qs.B0 for qs in all_lec]
    jk_m_res = [qs.m_res for qs in all_lec]
    return jk_b0, jk_m_res


@cache_data('24c_fv_su2')
def get_fv_corrections():
    length = 24
    m_s = 0.04
    jk_b0, jk_m_res = get_pion_lec_su2_fv()
    NUM_LEC = 190
    light_delmsq = {k: covariant_delmsq_meas[k] for k in (0.005, 0.01)}
    filtered_del_m_sq = filter_del_m_sq(light_delmsq)
    padded = pad(filtered_del_m_sq, NUM_LEC)
    fvc = {}
    for x_block in padded.keys():
        m_1, m_3, q_1, q_3, m_4 = x_block
        m_1 = round(m_1, ndigits=9)
        m_3 = round(m_3, ndigits=9)
        m_4 = round(m_4, ndigits=9)
        log.debug("{}".format((m_1, m_3, m_4, q_1, q_3)))
        fvc[x_block] = [get_fvc(q_1, q_3, 0., 0., 0., m_1, m_3, m_4, m_4, m_s,
                                b0, mres, length)
                        for b0, mres in zip(jk_b0, jk_m_res)]
    return fvc


@cache_data('24c_fv_kaon_su2_002')
def get_fv_corrections_kaon_002():
    return get_fv_corrections_kaon(0.02)

@cache_data('24c_fv_kaon_su2_003')
def get_fv_corrections_kaon_003():
    return get_fv_corrections_kaon(0.03)


def get_fv_corrections_kaon(m_3):
    length = 24
    m_s = 0.04
    jk_b0, jk_m_res = get_pion_lec_su2_fv()
    num_lec = 190
    light_delmsq = {k: covariant_delmsq_meas[k] for k in (0.005, 0.01, 0.02,
                                                          0.03)}
    filtered_del_m_sq = filter_kaon_del_m_sq(light_delmsq, m_3)
    padded = pad(filtered_del_m_sq, num_lec)
    fvc = {}
    for x_block in padded.keys():
        m_1, m_3, q_1, q_3, m_4 = x_block
        if m_3 < m_1:
            m_1, m_3 = m_3, m_1
            q_1, q_3 = q_3, q_1
        new_key = m_1, m_3, q_1, q_3, m_4
        m_1 = round(m_1, ndigits=9)
        m_3 = round(m_3, ndigits=9)
        m_4 = round(m_4, ndigits=9)
        log.debug("{}".format((m_1, m_3, m_4, q_1, q_3)))
        fvc[new_key] = [get_fvc(q_1, q_3, 0., 0., 0., m_1, m_3, m_4, m_4, m_s,
                                b0, mres, length)
                        for b0, mres in zip(jk_b0, jk_m_res)]
    return fvc