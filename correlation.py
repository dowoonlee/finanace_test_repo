from scipy.stats import spearmanr, pearsonr, ks_2samp
import numpy as np

def masking(x1, y1, x2, y2):
    # match/mask
    mask1, mask2 = np.zeros(len(x1)), np.zeros(len(x2))

    j = 0
    for i, el in enumerate(x1):
        while  j<len(x2) and el > x2[j]:
            j += 1
        if el>x2[j]:
            pass
        elif el==x2[j]:#el == x2[j] : el in x2
            mask1[i] = 1
            mask2[j] = 1
    x1 = x1[mask1.astype(bool)]
    y1 = y1[mask1.astype(bool)]
    x2 = x2[mask1.astype(bool)]
    y2 = y2[mask2.astype(bool)]
    return x1, y1, x2, y2

def __moving_window(f, y1, y2, ws):
    if len(y1)!=len(y2):
        return False
    if len(y1)<ws:
        return False
    res = []
    for st in range(len(y1)-ws):
        d, _ = f(y1[st:st+ws], y2[st:st+ws])
        res.append(d)
    return np.array(res)

def get_spearman(y1, y2, ws):
    return __moving_window(spearmanr, y1, y2, ws)

def get_pearson(y1, y2, ws):
    return __moving_window(pearsonr, y1, y2, ws)


def get_ks(y, ws):
    ref = y[-ws:]
    res = []
    for st in range(len(y)-ws):
        inf = y[st:st+ws]
        d, _ = ks_2samp(ref/ref.max(), inf/inf.max())
        res.append(d)
    return np.array(res)



