from pyon.lib.fitting.base import FitMethod
import numpy as np


class SVDFitMethod(FitMethod):
    """
    Solves for x in Ax=b using linalg.lstsq
    """
    def fit(self, fit_obj, initial_value, bounds):
        a, b = fit_obj
        m = np.linalg.lstsq(a, b)
        return m