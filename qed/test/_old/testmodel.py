import unittest
from pyon.lib.fitting import fit_hadron
from pyon.runner.models import Model
from qed.test.testview import my_view


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
        self.my_view = my_view()
        self.my_model = MyModel()

    def test_create_model(self):
        self.assertTrue(self.my_model)

