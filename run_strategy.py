import os, sys, argparse
import pandas as pd
import backtrader as bt
from backtrader import Cerebro
from strategies.GoldenCross  import GoldenCross
from strategies.BuyHold  import BuyHold
#from strategies.MacdStratTalib import MacdStrat
from strategies.MacdStrat import MacdStrat

from strategies.MovingAverage import MovingAverage
from strategies.Sar import Sar
from strategies.AdxMacd import AdxMacd

from get_data import get_data


cerebro = bt.Cerebro()


symbol = 'TSLA' #CLDR'

prices = get_data(symbol, "01-01-2020","09-15-2020")
print(prices.head())

prices =  pd.read_csv(f'../datasets/data_1yr_sep/{symbol}.csv', index_col='Date', parse_dates=True)

print(prices.head())

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
    "moving_avg":MovingAverage,
    "sar":Sar,
    "adx_macd":AdxMacd
}

#check against - golden_cross, buy_hold, macd, moving_avg, sar
strategy = "sar"

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
    cerebro.plot()

