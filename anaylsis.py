import numpy as np
import pandas as pd
from astropy.time import Time
import matplotlib.pyplot as plt
from correlation import *

stock_symbol = "S&P500"
stock_list = pd.read_parquet("./dataset/stock/%s/stock_list.parquet"%stock_symbol)

ref = pd.read_parquet("./dataset/stock/%s/%s.parquet"%(stock_symbol, "AAPL"))
date_ref = Time(ref.index.to_numpy()).mjd
cls_ref = ref.Close.to_numpy()
window_sizes = {
            "1w" : 5, "2w" : 10, "1m":20,
            "3m" : 60, "6m" : 120, "1y": 5*52,
            "2y" : 5*52*2}




for i in range(1):#stock_list.shape[0]):
    company = stock_list.iloc[i, :]
    try:
        inf = pd.read_parquet("./dataset/stock/%s/%s.parquet"%(stock_symbol, company.Symbol))
    except FileNotFoundError:
        continue
    if inf.shape[0]<1:
        continue

    date_inf = Time(inf.index.to_numpy()).mjd
    cls_inf = inf.Close.to_numpy()

    x, y1, _, y2 = masking(date_ref, cls_ref, date_inf, cls_inf)

    for lb, ws in window_sizes.items():
        ks = get_ks(cls_ref, ws)
        pearson = get_pearson(y1, y2, ws)
        t, ks_, _, pearson = masking(date_ref[ws:], ks, x[ws:], pearson)
        
        spearman = get_spearman(y1, y2, ws)
        t, ks_, _, spearman = masking(date_ref[ws:], ks, x[ws:], spearman)

        pm = np.average(pearson, weights=ks_)
        sm = np.average(spearman, weights=ks_)
        print(lb, pm, sm)
    





    


