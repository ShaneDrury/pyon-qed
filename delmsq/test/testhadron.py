import os
from django.test import TestCase
from pyon.lib.fitting import fit_hadron
from pyon.lib.io import parsers
from pyon.lib.meson import PseudoscalarChargedMeson
from delmsq.lib.fitting import MinuitFitter
from delmsq.models import ChargedMeson, TimeSlice
import numpy as np


def parse_from_folder(folder):
    all_data = parsers.Iwasaki32cCharged().get_from_folder(folder)
    for d in all_data:
        re_dat = d.pop('data')
        im_dat = d.pop('im_data')
        time_slices = d.pop('time_slices')
        mes = ChargedMeson(**d)
        mes.save()
        for t, re, im in zip(time_slices, re_dat, im_dat):
            time_slice = TimeSlice(t=t, re=re, im=im)
            mes.data.add(time_slice)


def my_view():
    qs = ChargedMeson.objects.filter(charge_1=-1, charge_2=-1,
                                               mass_1=0.03, mass_2=0.03,
                                               source='GAM_5',
                                               sink='GAM_5')
    return qs


class HadronTests(TestCase):
    def setUp(self):
        self.mes = ChargedMeson

    def test_make_hadron(self):
        parse_from_folder(os.path.join(
            'delmsq', 'test', 'testfiles', 'correlators', 'f1'))
        qs = my_view()
        mes = PseudoscalarChargedMeson.from_queryset(qs)
        mes.sort()
        mes.fold()
        mes.scale()
        bnds = ((0., 1.), (0, None))
        fit_kwargs = dict(fit_range=np.array(range(7, 25+1)),
                          initial_value=dict(m=0.3212, c=1.65),
                          covariant=False,
                          bounds=bnds)
        fp = fit_hadron(mes, method=MinuitFitter, **fit_kwargs)
        ave_m = fp.average_params['m']
        self.assertAlmostEqual(ave_m, 0.3211, places=4)