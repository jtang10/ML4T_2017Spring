"""MC1-P1: Analyze a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import math

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    alloc_asset = []
    for i in range(len(syms)):
        # Calculate cr for each stock
        num_stock = sv * allocs[i] / prices[syms[i]][0]
        alloc_asset.append(num_stock)

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

    # Get daily portfolio value
    port_val_all = prices.copy() # add code here to compute daily portfolio values
    port_val_all *= alloc_asset
    port_val = port_val_all.sum(axis=1)
    port_val /= port_val[0]
    prices_SPY /= prices_SPY[0]

    # Get portfolio statistics (note: std_daily_ret = volatility)
    cr = calculate_cr(prices, alloc_asset)
    adr, sddr = calculate_adr_sddr(prices, alloc_asset)
    sr = calculate_sr(prices, alloc_asset, rfr, sf)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp)
        pass

    # Add code here to properly compute end value
    ev = port_val[-1]

    return cr, adr, sddr, sr, ev

def test_code():
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
    start_date = dt.datetime(2010,1,1)
    end_date = dt.datetime(2010,12,31)
    symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']
    allocations = [0.0, 0.0, 0.0, 1.0]
    start_val = 1000000
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    test_code()
