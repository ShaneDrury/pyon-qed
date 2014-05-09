from pyon.lib.meson import PseudoscalarChargedMeson
from pyon import Simulation
import unittest
from qed.test.testmodel import MyModel
from qed.test.testview import my_view


class MySimulation(Simulation):
    def __init__(self, model, view):
        super(MySimulation, self).__init__(model, view)
        self.hadron = PseudoscalarChargedMeson.from_view(self.view)
        self.hadron.sort()
        self.hadron.fold()
        self.hadron.scale()

    def do_simulation(self):
        action = self.model.main()
        return action(self.hadron, **self.simulation_params)


class TestSimulation(unittest.TestCase):
    def setUp(self):
        self.my_view = my_view()
        self.my_model = MyModel()
        sim = MySimulation
        self.my_sim = sim(self.my_model, self.my_view)
        bnds = ((0., 1.), (0, None))
        self.my_sim.set_simulation_params(fit_range=range(9, 32+1),
                                          initial_value=[0.3212, 1.654],
                                          covariant=True,
                                          bounds=bnds)

    def test_create_simulation(self):
        self.assertTrue(self.my_model)

    def test_get_simulation_results(self):
        fp = self.my_sim.get_results()
        fit_params = fp.average_params
        self.assertTrue(fit_params is not None)
        mass = fit_params['m']
        c = fit_params['c']
        self.failUnlessAlmostEqual(mass, 0.32120951002753384, delta=1e-6)
        self.failUnlessAlmostEqual(c, 1.6542423508883226, delta=1e-6)