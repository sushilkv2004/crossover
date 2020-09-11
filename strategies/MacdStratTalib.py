__author__ = 'skv'
import math
import backtrader as bt


class MacdStrat(bt.Strategy):
    results = []
    # max_roi = 0
    # max_fast = 0
    # max_slow = 0

    params = (
        # Standard MACD Parameters
        ('fast', 12),
        ('slow', 26),
        ('macdsig', 9),
        ('order_pct', 0.95),
    )

    def __init__(self):
        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=self.p.fast,
                                       period_me2=self.p.slow,
                                       period_signal=self.p.macdsig)

        self.size = 0
        self.roi = 0

    def start(self):
        self.val_start = self.broker.get_cash()  # keep the starting cash
        print(help(self.macd))

    def next(self):


        if self.position.size == 0:
            if self.macd[0] > 0:
                amount_to_invest = (self.p.order_pct * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)

                # print("Buy {} shares of {} at {}".format(self.size, self.p.ticker, self.data.close[0]))
                self.buy(size=self.size)
                print(f'----------Buy executed @{self.data.close}-------')

        if self.position.size > 0:
            if self.macd[0] < 0:
                # print("Sell {} shares of {} at {}".format(self.size, self.p.ticker, self.data.close[0]))
                self.close()
                print(f'----------Close executed @{self.data.close}-------')


    def stop(self):
        # calculate the actual returns
        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        print('{}-{}:'.format(self.params.fast, self.params.slow), end="")

        print(' ROI:        {:.2f}%'.format(100.0 * self.roi))

        MacdStrat.results.append((self.params.fast, self.params.slow, round(100.0 * self.roi, 2)))


    @classmethod
    def show_max(cls):
        # print("BEST: {}-{} : {:.2f}%".format(cls.max_fast, cls.max_slow, 100.0 * cls.max_roi)
        # print(sorted(cls.max_res, key=cls.max_res[]))
        cls.results.sort(key=lambda x: x[2], reverse=True)
        print("*"*20)
        for i, result in enumerate(cls.results, 1):
            print(i,":", result)
        print("*"*20)

        return cls.results[0]

"""Results1 : 
20 year : 
Best params: fast=17, slow=36, roi=125.14
1 : (17, 36, 125.14)
2 : (16, 38, 125.0)
3 : (17, 38, 121.71)
4 : (15, 38, 121.66)
5 : (18, 34, 120.89)


5 year:
Best params: fast=15, slow=18, roi=58.52
1 : (15, 18, 58.52)
2 : (12, 16, 57.18)
3 : (14, 18, 56.25)
4 : (13, 20, 56.04)
5 : (11, 22, 55.83)
122 : (13, 26, 37.77)

2 years:
Best params: fast=9, slow=12, roi=40.01
1 : (9, 12, 40.01)
2 : (8, 12, 38.81)
3 : (9, 10, 38.8)
4 : (7, 14, 38.71)
5 : (7, 12, 37.83)
157 : (13, 26, 17.18)


1 year:
Best params: fast=13, slow=30, roi=21.15
1 : (13, 30, 21.15)
2 : (12, 32, 21.15)
3 : (11, 34, 21.15)
4 : (10, 36, 21.15)
5 : (9, 38, 20.72)

151 : (13, 26, 11.7)

********************2 yrs
Best params: fast=10, slow=18, roi=28.72

1 : (10, 18, 28.72)
2 : (9, 20, 28.34)
3 : (8, 22, 27.67)
4 : (13, 18, 26.65)
5 : (14, 18, 26.32)
********************

"""