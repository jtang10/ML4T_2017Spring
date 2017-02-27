import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality

# Here is some examples of how to process the data
# df.ix['2010-01-01':'2010-01-31'] Jan's data

sd = dt.datetime(2010,1,1)
ed = dt.datetime(2010,12,31)
syms = ['GOOG','AAPL','GLD','XOM']
allocs=[0.2,0.3,0.4,0.1]
sv=1000000
rfr=0.0
sf=252.0
gen_plot=False

# Read in adjusted closing prices for given symbols, date range
dates = pd.date_range(sd, ed)
prices_all = get_data(syms, dates)  # automatically adds SPY
prices = prices_all[syms]  # only portfolio symbols
prices_SPY = prices_all['SPY']  # only SPY, for comparison later

# Get the initial share for each stock at the starting date.
# print prices['AAPL'][-1]

alloc_asset = []
daily_returns = prices.copy()
for i in range(len(syms)):
    # Calculate cr for each stock
    num_stock = sv * allocs[i] / prices[syms[i]][0]
    alloc_asset.append(num_stock)

ev_total = prices.ix[-1, :] * alloc_asset
ev = ev_total.sum(axis=0)
cr = ev/sv - 1


# Calculate daily return
#print daily_returns[1:]
returns = prices.copy()
returns *= alloc_asset
returns_total = returns.sum(axis=1)
#print returns_total
adr = (returns_total / returns_total.shift(1)) - 1
adr[0] = 0
print adr.mean()
daily_returns = prices - prices.shift(1)
daily_returns.ix[0, :] = 0
# print daily_returns * alloc_asset
daily_returns *= alloc_asset
daily_returns_total = daily_returns.sum(axis=1)


print alloc_asset
print ev
print('cumulative return is %f' % (ev / sv -1))
#print daily_returns


# Get daily portfolio value
port_val = prices_SPY # add code here to compute daily portfolio values

# Get portfolio statistics (note: std_daily_ret = volatility)
cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats

# Compare daily portfolio value with SPY using a normalized plot
if gen_plot:
    # add code to plot here
    df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
    pass

# Add code here to properly compute end value
ev = sv

'''
print "Start Date:", sd
print "End Date:", ed
print "Symbols:", syms
print "Allocations:", allocs
print "Sharpe Ratio:", sr
print "Volatility (stdev of daily returns):", sddr
print "Average Daily Return:", adr
print "Cumulative Return:", cr
'''