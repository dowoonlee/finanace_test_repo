import numpy as np
from scipy.interpolate import interp1d

def __interpolation(x, y, n):
    f = interp1d(x, y, kind="cubic")
    nx = np.linspace(x.min(), x.max(), n)
    ny = f(nx)
    return nx, ny

def preprocess(xy1, xy2):
    x1, y1 = xy1
    x2, y2 = xy2
    n = np.max([len(x1), len(x2)])
    x1, y1 = __interpolation(x1, y1, n)
    x2, y2 = __interpolation(x2, y2, n)
    return (x1, y1), (x2, y2)
    

def dtw(x, x_prime, q=2):
    def d(p1, p2):
        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    R = np.zeros((len(x), len(x_prime)))
    for i in range(len(x)):
        for j in range(len(x_prime)):
            R[i, j] = d(x[i], x_prime[j]) ** q
            if i > 0 or j > 0:
                R[i, j] += min(
                    R[i-1, j  ] if i > 0             else np.inf,
                    R[i  , j-1] if j > 0             else np.inf,
                    R[i-1, j-1] if (i > 0 and j > 0) else np.inf
                    # Note that these 3 terms cannot all be
                    # inf if we have (i > 0 or j > 0)
                )

    return R[-1, -1] ** (1. / q)