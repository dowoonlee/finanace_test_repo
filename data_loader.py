import yfinance as yf
from astropy.time import Time

def getData(company, start, end):
    stockData = yf.download(company, start, end)
    stockData["Daily Return"] = stockData['Adj Close'].pct_change()
    stockData["Daily Return"][0] = 0
    stockData["Time"] = Time(stockData.index.to_numpy()).mjd
    stockData = stockData.drop(columns = ["Open", "High", "Low"]).reset_index(drop=True)
    return stockData


def test(company):
    stockData = yf.Ticker(company)
    print(stockData.analyst_price_target)
    return



