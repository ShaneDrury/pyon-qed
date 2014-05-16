import os
from unittest import skip
from django.test import TestCase
from pyon.lib.io import parsers
from delmsq.models import ChargedMeson32c, TimeSlice


def parse_from_folder(folder, parser):
    all_data = parser.get_from_folder(folder)
    for d in all_data:
        re_dat = d.pop('data')
        im_dat = d.pop('im_data')
        time_slices = d.pop('time_slices')
        mes = ChargedMeson32c(**d)
        mes.save()
        for t, re, im in zip(time_slices, re_dat, im_dat):
            time_slice = TimeSlice(t=t, re=re, im=im)
            mes.data.add(time_slice)


def my_view():
    qs = ChargedMeson32c.objects.filter(charge_1=-1, charge_2=-1,
                                               mass_1=0.03, mass_2=0.03,
                                               source='GAM_5',
                                               sink='GAM_5')
    return qs


class ViewTests(TestCase):
    def setUp(self):
        self.mes = ChargedMeson32c
    @skip('slow')
    def test_filter(self):
        parse_from_folder(os.path.join(
            'delmsq', 'test', 'testfiles', 'correlators', 'f1'),
            parsers.Iwasaki32cCharged())
        qs = my_view()
        self.assertEqual(len(qs), 131)