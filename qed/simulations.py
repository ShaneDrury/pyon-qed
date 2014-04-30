import logging
from pyon import Simulation, register, registered_models, registered_views
from pyon.lib.fitting import ScipyFitter
from pyon.lib.meson import PseudoscalarChargedMeson
from qed.lib.fitting import MinuitFitter


@register.simulation('mu0.0042')
class MySim(Simulation):
    def __init__(self):
        model = registered_models['all del m sq'](fitter=MinuitFitter)
        charged = registered_views['charged']()
        uncharged = registered_views['uncharged']()
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
        self.simulation_params = dict(fit_range=range(7, 25+1),
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
