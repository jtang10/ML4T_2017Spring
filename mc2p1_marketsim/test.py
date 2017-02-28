import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
import math

orders_file = "./orders/orders.csv"
start_val = 1000000
rfr=0.0
sf=252.0

orders = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['NaN'])
orders = orders.sort_index()
#print type(orders.index.values[0])
#orders.index = pd.to_datetime(orders.index)
#print type(orders.index.values[0])

# Get the start date and end date for one order book
sd = orders.index.values[0]
ed = orders.index.values[-1]
#print sd, ed

# Get all the stocks traded
symbols = orders.ix[:, 0]
symbols = list(set(symbols))
#print type(symbols), symbols

# Get all the prices needed for this order book
dates = pd.date_range(sd, ed)
prices_all = get_data(symbols, dates)
prices_all['Cash']=np.ones(prices_all.shape[0])

# Initialize another dataframe to store all the traded shares
shares_all=prices_all*0.0
shares_all.iloc[0,-1]=start_val
#print shares_all

for i, row in orders.iterrows():
    stock_name = row[0]
    stock_price = prices_all[stock_name].ix[i]
    stock_shares = row[2]
    if row[1] == "BUY":
        buy = 1
    else:
        buy = -1
    shares_all.loc[i, stock_name] += stock_shares * buy
    shares_all.loc[i, "Cash"] += stock_shares * stock_price * buy * -1

# print shares_all

for i in range(1, shares_all.shape[0]):
    for j in range(shares_all.shape[1]):
        shares_all.iloc[i, j] += shares_all.iloc[i - 1, j]

# print shares_all

port_val = prices_all * shares_all
port_val['port_val'] = port_val.sum(axis=1)
port_val['daily_returns'] = port_val['port_val'] / port_val['port_val'].shift(1) - 1
port_val['daily_returns'][0] = 0
print port_val

cr = port_val.ix[-1, -2] / port_val.ix[0, -2] - 1
adr = port_val['daily_returns'][1:].mean()
sddr = port_val['daily_returns'][1:].std()
daily_rf = math.pow(1 + rfr, 1/sf) - 1
sr = (adr - daily_rf) / sddr * math.sqrt(sf)
print "Cumulative return is", cr
print "Average daily return is", adr
print "Standard deviation of daily return is", sddr
print "Sharpe ratio is", sr
