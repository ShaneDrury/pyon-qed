# Create your measurements here
from su2.lec import get_qed_lec_pion_fv
from su2.lib.fv import get_fv_corrections

measurements = [
    {
        'name': 'su2 fv corrections',
        'measurement': get_fv_corrections,
        # 'template_name': 'path/to/meas/template.html'
        # 'plots': some_plot_func,
    },
    {
        'name': 'QED LEC Pion',
        'measurement': get_qed_lec_pion_fv,
        # 'template_name': 'path/to/meas/template.html'
        # 'plots': some_plot_func,
    },
]
