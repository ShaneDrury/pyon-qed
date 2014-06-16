# Create your measurements here
from su3.views import get_del_m_sq


def find_qed_lec():
    filtered_del_m_sq = get_del_m_sq()




measurements = [
    {
        'name': 'qed_lec',
        'measurement': find_qed_lec,
        'template_name': 'su3/index.html',
    }
]
