# Create your views here.
import logging

from meas24c.measurements import uncovariant_delmsq_meas

log = logging.getLogger(__name__)


def get_del_m_sq(covariant=False):
    if not covariant:
        all_del_m_sq = uncovariant_delmsq_meas
    else:
        all_del_m_sq = covariant_delmsq_meas

    filtered_delmsq = {}

    for m_l, v in all_del_m_sq.items():
        results = v()
        for k, delmsq in results.items():
            ml1, ml2, q1, q2 = k
            if ml1 <= 0.01 and ml2 <= 0.01:
                log.debug("Accepting ml={} {}, {}".format(m_l, (ml1, ml2),
                                                          (q1, q2)))
                filtered_delmsq[k] = delmsq
    return filtered_delmsq