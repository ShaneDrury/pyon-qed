from meas24c.measurements import uncovariant_delmsq_meas
from su3.views import filter_del_m_sq


def find_qed_lec():
    light_delmsq = {k: uncovariant_delmsq_meas[k] for k in (0.005, 0.01, 0.02, 0.03)}
    # filtered_del_m_sq = filter_del_m_sq(uncovariant_delmsq_meas)
    filtered_del_m_sq = filter_del_m_sq(light_delmsq)
    for xx in filtered_del_m_sq.keys():
        print(xx)
    exit()

measurements = [
    {
        'name': 'qed_lec',
        'measurement': find_qed_lec,
        'template_name': 'su3/index.html',
    }
]
