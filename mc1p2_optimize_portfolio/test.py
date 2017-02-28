import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import scipy.optimize as spo
import math

sd=dt.datetime(2008,1,1)
ed=dt.datetime(2009,1,1)
syms=['GOOG','AAPL','GLD','XOM']
gen_plot=False

# Read in adjusted closing prices for given symbols, date range
dates = pd.date_range(sd, ed)
prices_all = get_data(syms, dates)  # automatically adds SPY
prices = prices_all[syms]  # only portfolio symbols
prices_SPY = prices_all['SPY']  # only SPY, for comparison later


# find the allocations for the optimal portfolio
# note that the values here ARE NOT meant to be correct for a test case
allocs = np.asarray([1.0/len(syms) for i in range(len(syms))]) # add code here to find the allocations
sv = 1.0
rfr = 0.0
sf = 252.0

alloc_asset = []
for i in range(len(syms)):
    # Calculate cr for each stock
    num_stock = sv * allocs[i] / prices[syms[i]][0]
    alloc_asset.append(num_stock)
print alloc_asset

print allocs / prices.ix[0, :]

# Calculate cumulative return
def calculate_cr(prices, alloc_asset):
    returns = prices.copy()
    returns *= alloc_asset
    returns_total = returns.sum(axis=1)
    ev = returns_total[-1]
    cr = ev / sv - 1
    return cr

def calculate_adr_sddr(prices, alloc_asset):
    daily_returns = prices.copy()
    daily_returns *= alloc_asset
    daily_returns_total = daily_returns.sum(axis=1)
    # print daily_returns_total
    dr = (daily_returns_total / daily_returns_total.shift(1)) - 1
    dr[0] = 0
    adr = dr[1:].mean()
    sddr = dr[1:].std()
    return adr, sddr

def calculate_sr(prices, alloc_asset, rfr, sf):
    adr, sddr = calculate_adr_sddr(prices, alloc_asset)
    daily_rf = math.pow(1 + rfr, 1/sf) - 1
    sr = (adr - daily_rf) / sddr * math.sqrt(sf)
    return sr

cr = calculate_cr(prices, alloc_asset)
adr, sddr = calculate_adr_sddr(prices, alloc_asset)
sr = calculate_sr(prices, alloc_asset, rfr, sf)


# Get daily portfolio value
port_val_all = prices.copy()
port_val_all *= alloc_asset
port_val = port_val_all.sum(axis=1)
port_val /= port_val[0]
prices_SPY /= prices_SPY[0]

# Compare daily portfolio value with SPY using a normalized plot
if gen_plot:
    # add code to plot here
    df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
    plot_data(df_temp)
    pass

print "Start Date:", sd
print "End Date:", ed
print "Symbols:", syms
print "Allocations:", allocs
print "Sharpe Ratio:", sr
print "Volatility (stdev of daily returns):", sddr
print "Average Daily Return:", adr
print "Cumulative Return:", cr