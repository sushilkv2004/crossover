import os, sys, argparse
import pandas as pd
import backtrader as bt
from backtrader import Cerebro
from strategies.GoldenCross  import GoldenCross
from strategies.BuyHold  import BuyHold
from strategies.MacdStrat import MacdStrat
from strategies.MovingAverage import MovingAverage

cerebro = bt.Cerebro()

#prices = pd.read_csv('data/spy_2000-2020.csv', index_col='Date', parse_dates=True)
#prices = pd.read_csv('../datasets/daily/AMZN.csv', index_col='Date', parse_dates=True)


#prices = pd.read_csv('../datasets/data/spy_1yr.csv', index_col='Date', parse_dates=True)
#prices = pd.read_csv('../datasets/data/spy_2yrs.csv', index_col='Date', parse_dates=True)
#prices = pd.read_csv('../datasets/data/spy_5yrs.csv', index_col='Date', parse_dates=True)


symbol = 'CLDR'
#prices = pd.read_csv('../datasets/data/{}_5Yrs.csv'.format(symbol), index_col='Date', parse_dates=True)

prices =  pd.read_csv('../datasets/data/CLDR_max.csv', index_col='Date', parse_dates=True)


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
    "macd_opt":MacdStrat,
    "moving_avg":MovingAverage

}

strategy = "moving_avg"

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
        fast=range(8, 16, 1), slow=range(16,32,2),
    )
    cerebro.run(maxcpus=1)
    best_fast, best_slow, best_roi = MacdStrat.show_max()
    print('Best params: fast={}, slow={}, roi={}'.format(best_fast, best_slow, best_roi))
    """
    elif strategy == "macd":
        cerebro.addstrategy(strategy=strategies[strategy],fast=15, slow=30)
        cerebro.run()
        cerebro.plot()
    """

elif strategy == "moving_avg_opt":
    strats = cerebro.optstrategy(
        MovingAverage,
        fast=range(8, 16, 1), slow=range(16,32,2), ticker=symbol
    )
    cerebro.run(maxcpus=1)
    best_fast, best_slow, best_roi = MovingAverage.show_max()
    print('Best params: fast={}, slow={}, roi={}'.format(best_fast, best_slow, best_roi))

else:
    cerebro.addstrategy(strategy=strategies[strategy], ticker=symbol)
    cerebro.run()
    #cerebro.plot()

