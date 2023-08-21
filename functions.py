import numpy as np
from scipy.interpolate import interp1d

def __interpolation(x, y, nx):
    f = interp1d(x, y, kind="cubic")
    ny = f(nx)
    return nx, ny

def preprocess(xy1, xy2):
    x1, y1 = xy1
    x2, y2 = xy2
    n = np.max([len(x1), len(x2)])
    nx = np.linspace(min(x1.min(), x2.min()), max(x1.max(), x2.max()), n)
    x1, y1 = __interpolation(x1, y1, nx)
    x2, y2 = __interpolation(x2, y2, nx)
    return (x1, y1), (x2, y2)
    

