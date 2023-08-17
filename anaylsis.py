import numpy as np
import pandas as pd
from astropy.time import Time
import matplotlib.pyplot as plt


stock_symbol = "KOSPI"
stock_list = pd.read_parquet("./dataset/stock/%s/stock_list.parquet"%stock_symbol)


from scipy.stats import ks_2samp
def d_ks(x, window_size):
    ref = x[:window_size]
    res = []
    for i in range(len(x)-window_size):
        inf = x[i:i+window_size]
        d, _ = ks_2samp(ref/ref.max(), inf/inf.max())
        res.append(d)
    return np.array(res)


for row in range(stock_list.shape[0]):
    company = stock_list.iloc[row, :]
    df = pd.read_parquet("./dataset/stock/%s/%s.parquet"%(stock_symbol, company.Code))
    close = df.Close.to_numpy()
    date = Time(df.index.to_numpy()).mjd

    

    plt.figure()
    ax = plt.subplot()
    axt = plt.twinx(ax)
    ax.plot(date, close, color="black")
    for ws in [105, 210, 420]:
        d = d_ks(close, ws)
        date_ = date[ws:]
        axt.plot(date_, d, label=ws)
    axt.legend(loc='best')
    ax.set_xticks([date.min()+365*i for i in range(int((date.max()-date.min())/365)+1)])
    ax.set_xlim(date.min(), date.max())
    ax.grid(axis="x")
    plt.show()
    break

