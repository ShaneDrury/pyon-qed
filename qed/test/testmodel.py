import unittest
from pyon.lib.fitting import fit_hadron
from pyon.runner import register
from pyon.runner.models import Model
from pyon.runner.register import registered_models, registered_views


@register.model('my_model')
class MyModel(Model):
    def __init__(self):
        pass

    @staticmethod
    def fit_hadron(hadron, **kwargs):
        return fit_hadron(hadron, **kwargs)

    def main(self):
        """
        Returns the function
        """
        return self.fit_hadron


class TestModel(unittest.TestCase):
    def setUp(self):
        self.my_view = registered_views['my_view']()
        self.my_model = registered_models['my_model']()

    def test_create_model(self):
        self.assertTrue(self.my_model)

