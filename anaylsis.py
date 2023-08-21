import numpy as np
import pandas as pd
from astropy.time import Time
import matplotlib.pyplot as plt
from correlation import *
from functions import *

stock_symbol = "S&P500"
ref_symbol = "AAPL"

class LookAlike():
    def __init__(self, stock_symbol, ref_symbol):
        self.root_direc = "./dataset/stock/%s/"%stock_symbol
        ref = pd.read_parquet(self.root_direc+"/%s.parquet"%ref_symbol)
        date_ref = Time(ref.index.to_numpy()).mjd
        cls_ref = ref.Close.to_numpy()
        self.x1 = (date_ref, cls_ref)
        self.ws = {
            "1w" : 5, "2w" : 10, "1m":20,
            "3m" : 60, "6m" : 120, "1y": 5*52,
            "2y" : 5*52*2}
        self.stock_list = pd.read_parquet(self.root_direc+"/stock_list.parquet")

    def reset(self, ref_symbol):
        ref = pd.read_parquet(self.root_direc+"/%s.parquet"%ref_symbol)
        date_ref = Time(ref.index.to_numpy()).mjd
        cls_ref = ref.Close.to_numpy()
        self.x1 = (date_ref, cls_ref)
    
    def run(self):
        symbol_list = self.stock_list.Symbol.to_numpy()
        for i, symbol_inf in enumerate(symbol_list):
            try:
                inf = pd.read_parquet(self.root_direc + "%s.parquet"%symbol_inf)
                x2 = (Time(inf.index.to_numpy()).mjd, inf.Close.to_numpy())
            except:
                continue
            for j, ws in enumerate(self.ws):
                xy1 = (self.x1[0][:-ws], self.x1[1][:-ws])
                for k in range(len(x2[0])-ws):
                    xy2 = (x2[0][k:k+ws], x2[1][k:k+ws])
                    nxy1, nxy2 = preprocess(xy1, xy2)
                    c2s = 

        

lal = LookAlike(stock_symbol=stock_symbol, ref_symbol=ref_symbol)
lal.run()