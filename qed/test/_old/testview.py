import unittest
from qed.test.testsource import MySource


def my_view():
    src = MySource()
    filtered_data = src.filter(source='GAM_5', sink='GAM_5',
                               masses=(0.03, 0.03))
    return filtered_data


class TestView(unittest.TestCase):
    def setUp(self):
        self.my_view = my_view()

    def test_create_view(self):
        self.assertTrue(self.my_view)