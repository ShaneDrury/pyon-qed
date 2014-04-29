import unittest
from pyon.runner import register
from pyon.runner.register import registered_sources, registered_views


@register.view('my_view')
def my_view():
    src = registered_sources['my_source']()
    filtered_data = src.filter(source='GAM_5', sink='GAM_5',
                               masses=(0.03, 0.03))
    return filtered_data


class TestView(unittest.TestCase):
    def setUp(self):
        self.my_view = registered_views['my_view']

    def test_create_view(self):
        self.assertTrue(self.my_view)