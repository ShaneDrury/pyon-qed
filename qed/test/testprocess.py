import os
from unittest import skip
from pyon.lib.io import parsers
from django.test import TestCase
from qed.models import Iwasaki32cChargedMeson, TimeSlice


def parse_from_folder(folder, parser):
    all_data = parser.get_from_folder(folder)
    for d in all_data:
        re_dat = d.pop('data')
        im_dat = d.pop('im_data')
        time_slices = d.pop('time_slices')
        mes = Iwasaki32cChargedMeson(**d)
        mes.save()
        for t, re, im in zip(time_slices, re_dat, im_dat):
            time_slice = TimeSlice(t=t, re=re, im=im)
            mes.data.add(time_slice)


class ProcessTests(TestCase):
    def setUp(self):
        self.mes = Iwasaki32cChargedMeson
        self.parser = parsers.Iwasaki32cCharged()

    @skip('slow')
    def test_add_to_db(self):
        parse_from_folder(os.path.join(
            'qed', 'test', 'testfiles', 'correlators', 'f1'), self.parser)
        mes = self.mes.objects.all()[0]
        dat = mes.data.all()[0]
        self.assertEqual(dat.re, 1064639.0)