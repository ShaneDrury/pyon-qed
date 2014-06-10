from pyon.lib.fitting import FitterBase
import numpy as np


class SVDFitter(FitterBase):
    """
    Minimizes by using `linalg.lstsq` i.e solving for x:
    a^T a x = a^T b
    """
    def fit(self):
        pass

    @staticmethod
    def minimize(a, b):
        """
        Minimizes ax=b.
        :param a:
        :param b:
        :return:
        """
        m = np.linalg.lstsq(a, b)
        return m
