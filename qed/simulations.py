import logging
from pyon.runner.simulations import Simulation
from pyon.lib.meson import PseudoscalarChargedMeson
from qed.lib.fitting import MinuitFitter
import numpy as np
#from qed.models import AllDelMSq
#from qed.views import charged_mesons, uncharged_mesons


class MySim(Simulation):
    def __init__(self):
        model = AllDelMSq(fitter=MinuitFitter)
        charged = charged_mesons()
        uncharged = uncharged_mesons()
        super(MySim, self).__init__(model, [charged, uncharged])

        self.charged_hadrons = {}
        for k, v in charged.items():
            had = PseudoscalarChargedMeson.from_view(v)
            had.sort()
            had.fold()
            had.scale()
            self.charged_hadrons[k] = had

        self.uncharged_hadrons = {}
        for k, v in uncharged.items():
            had = PseudoscalarChargedMeson.from_view(v)
            had.sort()
            had.fold()
            had.scale()
            self.uncharged_hadrons[k] = had

        bnds = ((0., 1.), (0, None))
        self.simulation_params = dict(fit_range=np.array(range(7, 25+1)),
                                      initial_value=dict(m=0.18, c=1.39432),
                                      #initial_value=[0.18, 1.39432],
                                      covariant=False,
                                      bounds=bnds)

    def do_simulation(self):
        logging.info("Starting simulation")
        action = self.model.main()
        return action(self.charged_hadrons, self.uncharged_hadrons,
                      self.simulation_params, self.simulation_params)

    def get_plots(self):
        return None

