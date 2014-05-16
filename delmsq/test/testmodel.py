# from django.conf import settings
# settings.configure()

"""
Run tests with `python djangomanage.py test`
"""

from django.test import TestCase
from delmsq.models import ChargedMeson32c, TimeSlice


class ModelTests(TestCase):
    def setUp(self):
        self.mes = ChargedMeson32c
        self.data = [1., 2., 3.]
        im_data = [0., 0., 0.]
        t_range = range(len(self.data))
        mes = ChargedMeson32c(source='GAM_5',
                                     sink='GAM_5',
                                     mass_1=0.03,
                                     mass_2=0.03,
                                     charge_1=-1,
                                     charge_2=1,
                                     config_number=1000)
        mes.save()
        for t, re, im in zip(t_range, self.data, im_data):
            time_slice = TimeSlice(t=t, re=re, im=im)
            mes.data.add(time_slice)

    def tearDown(self):
        pass

    def test_model_get_record(self):
        mes = self.mes.objects.all()[0]
        dat = mes.data.all()[0]
        self.assertTrue(dat.re, self.data[0])