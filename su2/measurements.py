# Create your measurements here
from su2.lec import get_qed_lec_pion_fv, get_qed_lec_kaon_fv_003, \
    get_qed_lec_kaon_fv_002
from su2.lib.fv import get_fv_corrections, get_fv_corrections_kaon
from su2.masses import get_su2_masses

measurements = [
    {
        'name': 'su2 fv corrections',
        'measurement': get_fv_corrections,
        # 'template_name': 'path/to/meas/template.html'
        # 'plots': some_plot_func,
    },
    {
        'name': 'su2 fv corrections kaon',
        'measurement': get_fv_corrections_kaon,
        # 'template_name': 'path/to/meas/template.html'
        # 'plots': some_plot_func,
    },
    {
        'name': 'QED LEC Pion',
        'measurement': get_qed_lec_pion_fv,
        # 'template_name': 'path/to/meas/template.html'
        # 'plots': some_plot_func,
    },
    {
        'name': 'QED LEC Kaon 002',
        'measurement': get_qed_lec_kaon_fv_002,
        # 'template_name': 'path/to/meas/template.html'
        # 'plots': some_plot_func,
    },
    {
        'name': 'QED LEC Kaon 003',
        'measurement': get_qed_lec_kaon_fv_003,
        # 'template_name': 'path/to/meas/template.html'
        # 'plots': some_plot_func,
    },
    {
        'name': 'su2 masses',
        'measurement': get_su2_masses,
        # 'template_name': 'path/to/meas/template.html'
        # 'plots': some_plot_func,
    },

]
