import numpy as np
import FinanceDataReader as fdr
from astropy.time import Time
import os


stock_symbol = "KOSPI"
start_date = "2010-01-01"
stock_list = fdr.StockListing(stock_symbol)
# stock_list.to_parquet("./dataset/stock/%s/stock_list.parquet"%stock_symbol, index=False)
for row in range(stock_list.shape[0]):
    company = stock_list.iloc[row, :]
    df = fdr.DataReader(company.Code, start=start_date)
    df.to_parquet("./dataset/stock/%s/%s.parquet"%(stock_symbol, company.Code))