import os, sys, argparse
import pandas as pd
import backtrader as bt
from backtrader import Cerebro
from strategies.GoldenCross  import GoldenCross
from strategies.BuyHold  import BuyHold
from strategies.MacdStrat import MacdStrat
from strategies.MovingAverage import MovingAverage
from strategies.Sar import Sar
from strategies.AdxMacd import AdxMacd

from get_data import get_data


import math


def run(symbol, prices, strategy):

    # initialize the Cerebro engine
    cerebro = Cerebro()
    cerebro.broker.setcash(100000)

    # add OHLC data feed
    feed = bt.feeds.PandasData(dataname=prices)
    cerebro.adddata(feed)

    cerebro.addstrategy(strategy=strategy, ticker=symbol)
    cerebro.run()
    #cerebro.plot()

def buy_hold(prices):

    buy_price = prices.Close[0]
    sell_price = prices.Close[len(prices) - 1]

    val_start = 100000
    order_pct = .95
    amount_to_invest = (order_pct * val_start)
    size = math.floor(amount_to_invest / buy_price)

    cash = val_start - size*buy_price
    val_final = cash + size*sell_price
    roi = (val_final / val_start) - 1.0

    trade_count = 1

    print('  Strt={} End={} Traded={} ROI={:.2f}%'.format(val_start,val_final, trade_count, 100.0 * roi))


if __name__ == '__main__':

    strategies_dict = {
        "golden_cross": GoldenCross,
        "buy_hold": BuyHold,
        "macd": MacdStrat,
        "moving_avg": MovingAverage,
        "sar": Sar,
        "adx_macd": AdxMacd
    }

    # check against - golden_cross, buy_hold, macd, moving_avg, sar

    symbols = ['SPY', 'COF', 'AMZN', 'AAPL', 'DIS', 'NVDA','SBUX','GOOGL','UBER', 'TSLA']
    stragies = ["moving_avg", 'macd', 'adx_macd', 'sar']

    start_dates = ["01-01-2020", "01-01-2019", "01-01-2018", "01-01-2015"]
    end_date = "09-17-2020"
    for symbol in symbols:
        print("*"*20, symbol, "*"*20)
        for start_date in start_dates:
            prices = get_data(symbol, start_date,end_date)
            buy_price = prices.Close[0]
            sell_price = prices.Close[len(prices) - 1]
            print("\n",prices.index[0], buy_price, ":", prices.index[len(prices) - 1], sell_price)
            #pd.read_csv(f'../datasets/data_5yrs_sep/{symbol}.csv', index_col='Date', parse_dates=True)
            print(symbol, "Buy&Hold",end='')
            #print(prices.index[0], buy_price)
            #print(prices.index[len(prices) - 1], sell_price)

            buy_hold(prices)
            for strategy in stragies:
                print(symbol, strategy, end='')
                run(symbol, prices, strategies_dict[strategy])



"""
/usr/local/bin/python3.8 /Users/Sushil/Documents/GitHub/bt_talib/bt_stragegies/run_mult_strategy.py
******************** SPY ********************

 2020-01-02 00:00:00 324.8699951171875 : 2020-09-17 00:00:00 335.8399963378906
SPY Buy&Hold  Strt=100000 End=103203.24035644531 Traded=1 ROI=3.20%
SPY moving_avg  Strt=100000 End=111908.1982421875 Traded=2 ROI=11.91%
SPY macd  Strt=100000 End=112869.25358581543 Traded=6 ROI=12.87%
SPY adx_macd  Strt=100000 End=101206.7219543457 Traded=3 ROI=1.21%
SPY sar  Strt=100000 End=117462.6792602539 Traded=7 ROI=17.46%

 2019-01-02 00:00:00 250.17999267578125 : 2020-09-17 00:00:00 335.8399963378906
SPY Buy&Hold  Strt=100000 End=132465.14138793945 Traded=1 ROI=32.47%
SPY moving_avg  Strt=100000 End=119674.39016723633 Traded=5 ROI=19.67%
SPY macd  Strt=100000 End=119573.17031860352 Traded=18 ROI=19.57%
SPY adx_macd  Strt=100000 End=100579.29470825195 Traded=9 ROI=0.58%
SPY sar  Strt=100000 End=137677.59776306152 Traded=19 ROI=37.68%

 2018-01-02 00:00:00 268.7699890136719 : 2020-09-17 00:00:00 335.8399963378906
SPY Buy&Hold  Strt=100000 End=123675.71258544922 Traded=1 ROI=23.68%
SPY moving_avg  Strt=100000 End=116882.50869750977 Traded=8 ROI=16.88%
SPY macd  Strt=100000 End=124174.66868591309 Traded=30 ROI=24.17%
SPY adx_macd  Strt=100000 End=100159.57604980469 Traded=12 ROI=0.16%
SPY sar  Strt=100000 End=139069.28887939453 Traded=31 ROI=39.07%

 2015-01-02 00:00:00 205.42999267578125 : 2020-09-17 00:00:00 335.8399963378906
SPY Buy&Hold  Strt=100000 End=160249.42169189453 Traded=1 ROI=60.25%
SPY moving_avg  Strt=100000 End=128439.75090026855 Traded=20 ROI=28.44%
SPY macd  Strt=100000 End=134915.62854003906 Traded=63 ROI=34.92%
SPY adx_macd  Strt=100000 End=98737.51472473145 Traded=26 ROI=-1.26%
SPY sar  Strt=100000 End=142115.46046447754 Traded=68 ROI=42.12%
******************** COF ********************

 2020-01-02 00:00:00 103.61000061035156 : 2020-09-17 00:00:00 75.9800033569336
COF Buy&Hold  Strt=100000 End=74690.92251586914 Traded=1 ROI=-25.31%
COF moving_avg  Strt=100000 End=99542.30541992188 Traded=6 ROI=-0.46%
COF macd  Strt=100000 End=113799.83543777466 Traded=5 ROI=13.80%
COF adx_macd  Strt=100000 End=74233.62717437744 Traded=4 ROI=-25.77%
COF sar  Strt=100000 End=71807.15856170654 Traded=8 ROI=-28.19%

 2019-01-02 00:00:00 77.26000213623047 : 2020-09-17 00:00:00 75.9800033569336
COF Buy&Hold  Strt=100000 End=98426.88150024414 Traded=1 ROI=-1.57%
COF moving_avg  Strt=100000 End=89519.49670410156 Traded=12 ROI=-10.48%
COF macd  Strt=100000 End=117245.40478134155 Traded=16 ROI=17.25%
COF adx_macd  Strt=100000 End=68176.54975891113 Traded=9 ROI=-31.82%
COF sar  Strt=100000 End=73041.75155639648 Traded=20 ROI=-26.96%

 2018-01-02 00:00:00 99.61000061035156 : 2020-09-17 00:00:00 75.9800033569336
COF Buy&Hold  Strt=100000 End=77480.61261749268 Traded=1 ROI=-22.52%
COF moving_avg  Strt=100000 End=74955.01277160645 Traded=18 ROI=-25.04%
COF macd  Strt=100000 End=105511.37747955322 Traded=27 ROI=5.51%
COF adx_macd  Strt=100000 End=62287.91416931152 Traded=13 ROI=-37.71%
COF sar  Strt=100000 End=59366.68112945557 Traded=31 ROI=-40.63%

 2015-01-02 00:00:00 82.48999786376953 : 2020-09-17 00:00:00 75.9800033569336
COF Buy&Hold  Strt=100000 End=92506.99632263184 Traded=1 ROI=-7.49%
COF moving_avg  Strt=100000 End=87129.30283355713 Traded=28 ROI=-12.87%
COF macd  Strt=100000 End=114956.73987960815 Traded=59 ROI=14.96%
COF adx_macd  Strt=100000 End=50719.034576416016 Traded=28 ROI=-49.28%
COF sar  Strt=100000 End=68504.71559143066 Traded=67 ROI=-31.50%
******************** AMZN ********************

 2020-01-02 00:00:00 1898.010009765625 : 2020-09-17 00:00:00 3008.72998046875
AMZN Buy&Hold  Strt=100000 End=155535.99853515625 Traded=1 ROI=55.54%
AMZN moving_avg  Strt=100000 End=137424.35778808594 Traded=2 ROI=37.42%
AMZN macd  Strt=100000 End=118325.80126953125 Traded=4 ROI=18.33%
AMZN adx_macd  Strt=100000 End=151180.14892578125 Traded=2 ROI=51.18%
AMZN sar  Strt=100000 End=141635.72595214844 Traded=7 ROI=41.64%

 2019-01-02 00:00:00 1539.1300048828125 : 2020-09-17 00:00:00 3008.72998046875
AMZN Buy&Hold  Strt=100000 End=189645.5985107422 Traded=1 ROI=89.65%
AMZN moving_avg  Strt=100000 End=162950.06469726562 Traded=7 ROI=62.95%
AMZN macd  Strt=100000 End=147240.62353515625 Traded=13 ROI=47.24%
AMZN adx_macd  Strt=100000 End=148671.17736816406 Traded=6 ROI=48.67%
AMZN sar  Strt=100000 End=162585.05017089844 Traded=18 ROI=62.59%

 2018-01-02 00:00:00 1189.010009765625 : 2020-09-17 00:00:00 3008.72998046875
AMZN Buy&Hold  Strt=100000 End=243757.87768554688 Traded=1 ROI=143.76%
AMZN moving_avg  Strt=100000 End=186422.00463867188 Traded=9 ROI=86.42%
AMZN macd  Strt=100000 End=127832.16345214844 Traded=25 ROI=27.83%
AMZN adx_macd  Strt=100000 End=144077.68530273438 Traded=12 ROI=44.08%
AMZN sar  Strt=100000 End=143001.29858398438 Traded=29 ROI=43.00%

 2015-01-02 00:00:00 308.5199890136719 : 2020-09-17 00:00:00 3008.72998046875
AMZN Buy&Hold  Strt=100000 End=928964.467376709 Traded=1 ROI=828.96%
AMZN moving_avg  Strt=100000 End=675025.30859375 Traded=14 ROI=575.03%
AMZN macd  Strt=100000 End=210811.0866394043 Traded=53 ROI=110.81%
AMZN adx_macd  Strt=100000 End=200152.1293334961 Traded=30 ROI=100.15%
AMZN sar  Strt=100000 End=289451.2342224121 Traded=62 ROI=189.45%
******************** AAPL ********************

 2020-01-02 00:00:00 75.0875015258789 : 2020-09-17 00:00:00 110.33999633789062
AAPL Buy&Hold  Strt=100000 End=144594.40593719482 Traded=1 ROI=44.59%
AAPL moving_avg  Strt=100000 End=138989.72832489014 Traded=2 ROI=38.99%
AAPL macd  Strt=100000 End=144190.42846679688 Traded=5 ROI=44.19%
AAPL adx_macd  Strt=100000 End=148273.60223388672 Traded=2 ROI=48.27%
AAPL sar  Strt=100000 End=139218.9878501892 Traded=6 ROI=39.22%

 2019-01-02 00:00:00 39.47999954223633 : 2020-09-17 00:00:00 110.33999633789062
AAPL Buy&Hold  Strt=100000 End=270489.15229034424 Traded=1 ROI=170.49%
AAPL moving_avg  Strt=100000 End=242393.10917282104 Traded=4 ROI=142.39%
AAPL macd  Strt=100000 End=202915.81692504883 Traded=15 ROI=102.92%
AAPL adx_macd  Strt=100000 End=199515.72080230713 Traded=7 ROI=99.52%
AAPL sar  Strt=100000 End=212653.80810546875 Traded=19 ROI=112.65%

 2018-01-02 00:00:00 43.064998626708984 : 2020-09-17 00:00:00 110.33999633789062
AAPL Buy&Hold  Strt=100000 End=248341.36995315552 Traded=1 ROI=148.34%
AAPL moving_avg  Strt=100000 End=235038.1992378235 Traded=8 ROI=135.04%
AAPL macd  Strt=100000 End=221399.7493133545 Traded=26 ROI=121.40%
AAPL adx_macd  Strt=100000 End=234327.00692367554 Traded=12 ROI=134.33%
AAPL sar  Strt=100000 End=249873.19054031372 Traded=31 ROI=149.87%

 2015-01-02 00:00:00 27.332500457763672 : 2020-09-17 00:00:00 110.33999633789062
AAPL Buy&Hold  Strt=100000 End=388451.04818344116 Traded=1 ROI=288.45%
AAPL moving_avg  Strt=100000 End=289511.68637657166 Traded=18 ROI=189.51%
AAPL macd  Strt=100000 End=333563.80179977417 Traded=49 ROI=233.56%
AAPL adx_macd  Strt=100000 End=318452.3098449707 Traded=24 ROI=218.45%
AAPL sar  Strt=100000 End=281248.808965683 Traded=67 ROI=181.25%
******************** DIS ********************

 2020-01-02 00:00:00 148.1999969482422 : 2020-09-17 00:00:00 130.22000122070312
DIS Buy&Hold  Strt=100000 End=88474.82273864746 Traded=1 ROI=-11.53%
DIS moving_avg  Strt=100000 End=101185.07316589355 Traded=3 ROI=1.19%
DIS macd  Strt=100000 End=107995.47969055176 Traded=5 ROI=8.00%
DIS adx_macd  Strt=100000 End=114122.89044189453 Traded=2 ROI=14.12%
DIS sar  Strt=100000 End=96699.96433258057 Traded=7 ROI=-3.30%

 2019-01-02 00:00:00 108.97000122070312 : 2020-09-17 00:00:00 130.22000122070312
DIS Buy&Hold  Strt=100000 End=118508.75 Traded=1 ROI=18.51%
DIS moving_avg  Strt=100000 End=119106.5174407959 Traded=7 ROI=19.11%
DIS macd  Strt=100000 End=124924.43491363525 Traded=15 ROI=24.92%
DIS adx_macd  Strt=100000 End=135068.0924835205 Traded=6 ROI=35.07%
DIS sar  Strt=100000 End=112114.81021118164 Traded=17 ROI=12.11%

 2018-01-02 00:00:00 111.80000305175781 : 2020-09-17 00:00:00 130.22000122070312
DIS Buy&Hold  Strt=100000 End=115638.57844543457 Traded=1 ROI=15.64%
DIS moving_avg  Strt=100000 End=116925.67799377441 Traded=11 ROI=16.93%
DIS macd  Strt=100000 End=108965.81609344482 Traded=26 ROI=8.97%
DIS adx_macd  Strt=100000 End=120135.89053344727 Traded=11 ROI=20.14%
DIS sar  Strt=100000 End=104894.58311462402 Traded=27 ROI=4.89%

 2015-01-02 00:00:00 93.75 : 2020-09-17 00:00:00 130.22000122070312
DIS Buy&Hold  Strt=100000 End=136944.11123657227 Traded=1 ROI=36.94%
DIS moving_avg  Strt=100000 End=136609.16165924072 Traded=20 ROI=36.61%
DIS macd  Strt=100000 End=109852.00590515137 Traded=62 ROI=9.85%
DIS adx_macd  Strt=100000 End=139546.0085144043 Traded=23 ROI=39.55%
DIS sar  Strt=100000 End=89144.05152893066 Traded=61 ROI=-10.86%
******************** NVDA ********************

 2020-01-02 00:00:00 239.91000366210938 : 2020-09-17 00:00:00 498.5400085449219
NVDA Buy&Hold  Strt=100000 End=202158.85192871094 Traded=1 ROI=102.16%
NVDA moving_avg  Strt=100000 End=159939.00910949707 Traded=2 ROI=59.94%
NVDA macd  Strt=100000 End=111816.0615234375 Traded=6 ROI=11.82%
NVDA adx_macd  Strt=100000 End=136194.2927093506 Traded=4 ROI=36.19%
NVDA sar  Strt=100000 End=205988.4298400879 Traded=5 ROI=105.99%

 2019-01-02 00:00:00 136.22000122070312 : 2020-09-17 00:00:00 498.5400085449219
NVDA Buy&Hold  Strt=100000 End=352537.04510498047 Traded=1 ROI=252.54%
NVDA moving_avg  Strt=100000 End=247018.7081604004 Traded=4 ROI=147.02%
NVDA macd  Strt=100000 End=188581.74980163574 Traded=15 ROI=88.58%
NVDA adx_macd  Strt=100000 End=192040.7297821045 Traded=10 ROI=92.04%
NVDA sar  Strt=100000 End=284882.9617767334 Traded=16 ROI=184.88%

 2018-01-02 00:00:00 199.35000610351562 : 2020-09-17 00:00:00 498.5400085449219
NVDA Buy&Hold  Strt=100000 End=242414.44116210938 Traded=1 ROI=142.41%
NVDA moving_avg  Strt=100000 End=172902.28506469727 Traded=10 ROI=72.90%
NVDA macd  Strt=100000 End=96257.97918701172 Traded=28 ROI=-3.74%
NVDA adx_macd  Strt=100000 End=123488.76274108887 Traded=17 ROI=23.49%
NVDA sar  Strt=100000 End=151885.39010620117 Traded=28 ROI=51.89%

 2015-01-02 00:00:00 20.1299991607666 : 2020-09-17 00:00:00 498.5400085449219
NVDA Buy&Hold  Strt=100000 End=2357616.8342838287 Traded=1 ROI=2257.62%
NVDA moving_avg  Strt=100000 End=1089899.688123703 Traded=17 ROI=989.90%
NVDA macd  Strt=100000 End=219727.32287979126 Traded=62 ROI=119.73%
NVDA adx_macd  Strt=100000 End=309774.87458610535 Traded=32 ROI=209.77%
NVDA sar  Strt=100000 End=674087.1511745453 Traded=61 ROI=574.09%
******************** SBUX ********************

 2020-01-02 00:00:00 89.3499984741211 : 2020-09-17 00:00:00 86.75
SBUX Buy&Hold  Strt=100000 End=97236.20162200928 Traded=1 ROI=-2.76%
SBUX moving_avg  Strt=100000 End=112551.96504211426 Traded=2 ROI=12.55%
SBUX macd  Strt=100000 End=108560.93979644775 Traded=6 ROI=8.56%
SBUX adx_macd  Strt=100000 End=107902.30289459229 Traded=3 ROI=7.90%
SBUX sar  Strt=100000 End=127665.27265930176 Traded=7 ROI=27.67%

 2019-01-02 00:00:00 64.31999969482422 : 2020-09-17 00:00:00 86.75
SBUX Buy&Hold  Strt=100000 End=133106.68045043945 Traded=1 ROI=33.11%
SBUX moving_avg  Strt=100000 End=135522.45602416992 Traded=6 ROI=35.52%
SBUX macd  Strt=100000 End=112434.12712860107 Traded=16 ROI=12.43%
SBUX adx_macd  Strt=100000 End=135939.93897247314 Traded=7 ROI=35.94%
SBUX sar  Strt=100000 End=135064.67790603638 Traded=21 ROI=35.06%

 2018-01-02 00:00:00 57.630001068115234 : 2020-09-17 00:00:00 86.75
SBUX Buy&Hold  Strt=100000 End=147989.7582397461 Traded=1 ROI=47.99%
SBUX moving_avg  Strt=100000 End=156113.55423355103 Traded=9 ROI=56.11%
SBUX macd  Strt=100000 End=126705.50991821289 Traded=25 ROI=26.71%
SBUX adx_macd  Strt=100000 End=183625.09818649292 Traded=9 ROI=83.63%
SBUX sar  Strt=100000 End=156719.7046661377 Traded=33 ROI=56.72%

 2015-01-02 00:00:00 40.720001220703125 : 2020-09-17 00:00:00 86.75
SBUX Buy&Hold  Strt=100000 End=207387.9871520996 Traded=1 ROI=107.39%
SBUX moving_avg  Strt=100000 End=161201.62301635742 Traded=22 ROI=61.20%
SBUX macd  Strt=100000 End=106454.7472000122 Traded=57 ROI=6.45%
SBUX adx_macd  Strt=100000 End=133372.6070022583 Traded=24 ROI=33.37%
SBUX sar  Strt=100000 End=137964.49332427979 Traded=71 ROI=37.96%
******************** GOOGL ********************

 2020-01-02 00:00:00 1368.6800537109375 : 2020-09-17 00:00:00 1487.0400390625
GOOGL Buy&Hold  Strt=100000 End=108166.83898925781 Traded=1 ROI=8.17%
GOOGL moving_avg  Strt=100000 End=107124.80517578125 Traded=2 ROI=7.12%
GOOGL macd  Strt=100000 End=118090.25646972656 Traded=5 ROI=18.09%
GOOGL adx_macd  Strt=100000 End=107751.8310546875 Traded=4 ROI=7.75%
GOOGL sar  Strt=100000 End=113593.82995605469 Traded=8 ROI=13.59%

 2019-01-02 00:00:00 1054.6800537109375 : 2020-09-17 00:00:00 1487.0400390625
GOOGL Buy&Hold  Strt=100000 End=138912.39868164062 Traded=1 ROI=38.91%
GOOGL moving_avg  Strt=100000 End=135497.67529296875 Traded=4 ROI=35.50%
GOOGL macd  Strt=100000 End=132231.50720214844 Traded=13 ROI=32.23%
GOOGL adx_macd  Strt=100000 End=123041.96752929688 Traded=8 ROI=23.04%
GOOGL sar  Strt=100000 End=135504.12268066406 Traded=18 ROI=35.50%

 2018-01-02 00:00:00 1073.2099609375 : 2020-09-17 00:00:00 1487.0400390625
GOOGL Buy&Hold  Strt=100000 End=136417.046875 Traded=1 ROI=36.42%
GOOGL moving_avg  Strt=100000 End=133024.5235595703 Traded=6 ROI=33.02%
GOOGL macd  Strt=100000 End=122873.04333496094 Traded=26 ROI=22.87%
GOOGL adx_macd  Strt=100000 End=94670.09191894531 Traded=15 ROI=-5.33%
GOOGL sar  Strt=100000 End=112119.3310546875 Traded=29 ROI=12.12%

 2015-01-02 00:00:00 529.5499877929688 : 2020-09-17 00:00:00 1487.0400390625
GOOGL Buy&Hold  Strt=100000 End=271390.7191772461 Traded=1 ROI=171.39%
GOOGL moving_avg  Strt=100000 End=139377.4927368164 Traded=25 ROI=39.38%
GOOGL macd  Strt=100000 End=131942.5662841797 Traded=58 ROI=31.94%
GOOGL adx_macd  Strt=100000 End=96871.13262939453 Traded=30 ROI=-3.13%
GOOGL sar  Strt=100000 End=128904.2134399414 Traded=61 ROI=28.90%
******************** UBER ********************

 2020-01-02 00:00:00 30.989999771118164 : 2020-09-17 00:00:00 37.060001373291016
UBER Buy&Hold  Strt=100000 End=118604.55491065979 Traded=1 ROI=18.60%
UBER moving_avg  Strt=100000 End=84344.18977546692 Traded=5 ROI=-15.66%
UBER macd  Strt=100000 End=112804.4900188446 Traded=6 ROI=12.80%
UBER adx_macd  Strt=100000 End=119053.69609832764 Traded=3 ROI=19.05%
UBER sar  Strt=100000 End=126657.71107292175 Traded=7 ROI=26.66%

 2019-05-10 00:00:00 41.56999969482422 : 2020-09-17 00:00:00 37.060001373291016
UBER Buy&Hold  Strt=100000 End=89694.65383529663 Traded=1 ROI=-10.31%
UBER moving_avg  Strt=100000 End=85739.02982521057 Traded=7 ROI=-14.26%
UBER macd  Strt=100000 End=114041.29461479187 Traded=12 ROI=14.04%
UBER adx_macd  Strt=100000 End=129961.15282058716 Traded=5 ROI=29.96%
UBER sar  Strt=100000 End=132819.2779560089 Traded=15 ROI=32.82%

 2019-05-10 00:00:00 41.56999969482422 : 2020-09-17 00:00:00 37.060001373291016
UBER Buy&Hold  Strt=100000 End=89694.65383529663 Traded=1 ROI=-10.31%
UBER moving_avg  Strt=100000 End=85739.02982521057 Traded=7 ROI=-14.26%
UBER macd  Strt=100000 End=114041.29461479187 Traded=12 ROI=14.04%
UBER adx_macd  Strt=100000 End=129961.15282058716 Traded=5 ROI=29.96%
UBER sar  Strt=100000 End=132819.2779560089 Traded=15 ROI=32.82%

 2019-05-10 00:00:00 41.56999969482422 : 2020-09-17 00:00:00 37.060001373291016
UBER Buy&Hold  Strt=100000 End=89694.65383529663 Traded=1 ROI=-10.31%
UBER moving_avg  Strt=100000 End=85739.02982521057 Traded=7 ROI=-14.26%
UBER macd  Strt=100000 End=114041.29461479187 Traded=12 ROI=14.04%
UBER adx_macd  Strt=100000 End=129961.15282058716 Traded=5 ROI=29.96%
UBER sar  Strt=100000 End=132819.2779560089 Traded=15 ROI=32.82%
******************** TSLA ********************

 2020-01-02 00:00:00 86.052001953125 : 2020-09-17 00:00:00 423.42999267578125
TSLA Buy&Hold  Strt=100000 End=472127.92376708984 Traded=1 ROI=372.13%
TSLA moving_avg  Strt=100000 End=223289.61206054688 Traded=3 ROI=123.29%
TSLA macd  Strt=100000 End=144288.54327392578 Traded=7 ROI=44.29%
TSLA adx_macd  Strt=100000 End=168796.7579345703 Traded=2 ROI=68.80%
TSLA sar  Strt=100000 End=178257.0726776123 Traded=6 ROI=78.26%

 2019-01-02 00:00:00 62.02399826049805 : 2020-09-17 00:00:00 423.42999267578125
TSLA Buy&Hold  Strt=100000 End=653312.5774497986 Traded=1 ROI=553.31%
TSLA moving_avg  Strt=100000 End=659750.560760498 Traded=3 ROI=559.75%
TSLA macd  Strt=100000 End=341218.7075920105 Traded=17 ROI=241.22%
TSLA adx_macd  Strt=100000 End=443983.4277305603 Traded=4 ROI=343.98%
TSLA sar  Strt=100000 End=360026.6990966797 Traded=17 ROI=260.03%

 2018-01-02 00:00:00 64.10600280761719 : 2020-09-17 00:00:00 423.42999267578125
TSLA Buy&Hold  Strt=100000 End=632158.828994751 Traded=1 ROI=532.16%
TSLA moving_avg  Strt=100000 End=405021.0012664795 Traded=11 ROI=305.02%
TSLA macd  Strt=100000 End=302831.7352371216 Traded=26 ROI=202.83%
TSLA adx_macd  Strt=100000 End=349356.3164215088 Traded=8 ROI=249.36%
TSLA sar  Strt=100000 End=243957.30446243286 Traded=30 ROI=143.96%

 2015-01-02 00:00:00 43.86199951171875 : 2020-09-17 00:00:00 423.42999267578125
TSLA Buy&Hold  Strt=100000 End=921764.7052001953 Traded=1 ROI=821.76%
TSLA moving_avg  Strt=100000 End=475478.69702911377 Traded=24 ROI=375.48%
TSLA macd  Strt=100000 End=611383.7840652466 Traded=53 ROI=511.38%
TSLA adx_macd  Strt=100000 End=670992.9083328247 Traded=20 ROI=570.99%
TSLA sar  Strt=100000 End=203850.5650177002 Traded=68 ROI=103.85%

Process finished with exit code 0

"""