
import numpy as np


def colebrookfanning(eps, diam, re, error):
    # eps: rugosidad relativa [m]
    # diam: diametro de conducto [m]
    # re: numero de reynolds [N.A.]

    def colebrookwhiteg(eps, diam, re, x):
        g = -2*np.log10((eps/(3.7*diam)) + (2.51 * x / re))
        return g

    def colebrookwhitegprim(eps, diam, re, x):
        gprim = -(2/np.log(10))*((2.51 / re) /
                                 ((eps / (3.7 * diam)) + ((2.51 * x) / re)))
        return gprim

    delta = 1
    x = 1000

    while delta > 1e-8:
        delta = (colebrookwhiteg(eps, diam, re, x) - x) / \
            (colebrookwhitegprim(eps, diam, re, x) - 1)
        x -= delta

    f = np.power(1/x, 2)

    return f
