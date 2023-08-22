import numpy as np
import pandas as pd
from astropy.time import Time
from datetime import datetime
from data_loader import getData
from functions import *

company = "AAPL"
end = datetime.now()
start = datetime(end.year-10, end.month, end.day)
df = getData(
    company=company,
    start = start,
    end = end)

def series_to_supervised(data, n_in=5, n_out=5, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out, 1):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.metrics import mean_squared_error

def prediction(df, dt = 5):
    scaler = MinMaxScaler(feature_range=(0, 1))
    df_drop = df.drop(columns=["Time"]).values
    scaled = scaler.fit_transform(df_drop)
    reframed = series_to_supervised(scaled, n_in=dt, n_out=1)
    reframed = reframed.drop(columns=["var%d(t)"%i for i in [2,3,4]])
    values = reframed.values

    n_train = int(reframed.shape[0]*0.7)
    train = values[:n_train, :]
    test = values[n_train:, :]

    train_X, train_y = train[:, :-1], train[:, -1]
    test_X, test_y = test[:, :-1], test[:, -1]

    train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
    test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))

    model = Sequential()
    model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
    model.add(Dense(1))
    model.compile(loss='mae', optimizer='adam')

    history = model.fit(
        train_X,
        train_y,
        epochs=50,
        batch_size=72,
        validation_data=(test_X, test_y),
        verbose=2,
        shuffle=False)

    yhat = model.predict(test_X)
    test_X = test_X.reshape((test_X.shape[0], test_X.shape[1]*test_X.shape[2]))


    inv_yhat = np.concatenate((yhat, test_X[:, -3:]), axis=1)
    inv_yhat = scaler.inverse_transform(inv_yhat)
    inv_yhat = inv_yhat[:,0]

    test_y = test_y.reshape((len(test_y), 1))
    inv_y = np.concatenate((test_y, test_X[:, -3:]), axis=1)
    inv_y = scaler.inverse_transform(inv_y)
    inv_y = inv_y[:,0]

    
    rmse = np.sqrt(mean_squared_error(inv_y, inv_yhat))
    return inv_y, inv_yhat, rmse

import matplotlib.pyplot as plt
plt.plot(df.Time.to_numpy(), df.Close.to_numpy(), c="k")
ws = {"1w" : 5, "2w" : 10, "1m" : 20}
for lb, dt in ws.items():
    _, inv_yhat, rmse = prediction(df, dt = dt)
    plt.plot(df.Time.to_numpy()[-len(inv_yhat):], inv_yhat, label=lb)
plt.legend(loc='best')
plt.show()
print('Test RMSE: %.3f' % rmse)
