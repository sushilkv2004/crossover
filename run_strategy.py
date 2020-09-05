import os, sys, argparse
import pandas as pd
import backtrader as bt
from backtrader import Cerebro
from strategies.GoldenCross  import GoldenCross
from strategies.BuyHold  import BuyHold
from strategies.MacdStrat import MacdStrat

cerebro = bt.Cerebro()

prices = pd.read_csv('data/spy_2000-2020.csv', index_col='Date', parse_dates=True)
#prices = pd.read_csv('data/spy_5yrs.csv', index_col='Date', parse_dates=True)
#prices = pd.read_csv('data/spy_1yr.csv', index_col='Date', parse_dates=True)
#prices = pd.read_csv('data/spy_2yrs.csv', index_col='Date', parse_dates=True)


# initialize the Cerebro engine
cerebro = Cerebro()
cerebro.broker.setcash(100000)

# add OHLC data feed
feed = bt.feeds.PandasData(dataname=prices)
cerebro.adddata(feed)

strategies = {
    "golden_cross": GoldenCross,
    "buy_hold": BuyHold,
    "macd":MacdStrat,
    "macd_opt":MacdStrat
}

strategy = "macd_opt"

if strategy == "golden_cross_opt":
    cerebro.optstrategy(
        GoldenCross,
        fast=range(40, 60, 10), slow=range(160, 220, 20),
        #fast=range(10, 30, 10), slow=range(50, 90, 20),
    )
    cerebro.run(maxcpus=1)
    GoldenCross.show_max()
elif strategy == "macd_opt":
    strats = cerebro.optstrategy(
        MacdStrat,
        fast=range(5, 20, 1), slow=range(10,40,2),
    )
    cerebro.run(maxcpus=1)
    best_fast, best_slow, best_roi = MacdStrat.show_max()
    print('Best params: fast={}, slow={}, roi={}'.format(best_fast, best_slow, best_roi))

    cerebro.addstrategy(strategy=strategies[strategy],fast=best_fast, slow=best_slow)
    cerebro.run()
    cerebro.plot()

else:
    cerebro.addstrategy(strategy=strategies[strategy])
    cerebro.run()
    cerebro.plot()

