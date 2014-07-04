# Create your views here.
import logging

log = logging.getLogger(__name__)


def filter_del_m_sq(all_del_m_sq):
    filtered_delmsq = {}

    for m_l, v in all_del_m_sq.items():
        results = v()
        for k, delmsq in results.items():
            ml1, ml2, q1, q2 = k
            new_key = (ml1, ml2, q1, q2, m_l)
            if ml1 <= 0.01 and ml2 <= 0.01:
                log.debug("Accepting ml={} {}, {}".format(m_l, (ml1, ml2),
                                                          (q1, q2)))
                filtered_delmsq[new_key] = delmsq
    return filtered_delmsq