import math
import backtrader as bt


class GoldenCross(bt.Strategy):

    results = []
    #max_roi = 0
    #max_fast = 0
    #max_slow = 0

    params = (('fast', 50),
              ('slow', 160),
              ('order_pct', 0.95),
              ('ticker', 'SPY'))

    params_orig = (('fast', 50),
              ('slow', 200),
              ('order_pct', 0.95),
              ('ticker', 'SPY'))

    def __init__(self):
        self.fastma = bt.indicators.SimpleMovingAverage(
            self.data.close, 
            period=self.p.fast, 
            plotname='50 day'
        )

        self.slowma = bt.indicators.SimpleMovingAverage(
            self.data.close, 
            period=self.p.slow, 
            plotname='200 day'
        )

        self.crossover = bt.indicators.CrossOver(
            self.fastma, 
            self.slowma
        )
        self.size = 0
        self.roi = 0

    def start(self):
            self.val_start = self.broker.get_cash()  # keep the starting cash

    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:
                amount_to_invest = (self.p.order_pct * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)

                #print("Buy {} shares of {} at {}".format(self.size, self.p.ticker, self.data.close[0]))
                self.buy(size=self.size)
            
        if self.position.size > 0:
            if self.crossover < 0:
                #print("Sell {} shares of {} at {}".format(self.size, self.p.ticker, self.data.close[0]))
                self.close()

    def stop(self):
        # calculate the actual returns
        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        print('{}-{}:'.format(self.params.fast, self.params.slow), end="")

        print(' ROI:        {:.2f}%'.format(100.0 * self.roi))

        GoldenCross.results.append((self.params.fast, self.params.slow, round(100.0 * self.roi, 2)))
        """
        if self.roi > GoldenCross.max_roi:
            GoldenCross.max_roi = self.roi
            GoldenCross.max_fast = self.params.fast
            GoldenCross.max_slow = self.params.slow
        """

    @classmethod
    def show_max(cls):
        #print("BEST: {}-{} : {:.2f}%".format(cls.max_fast, cls.max_slow, 100.0 * cls.max_roi)
        #print(sorted(cls.max_res, key=cls.max_res[]))
        cls.results.sort(key=lambda x: x[2], reverse=True)
        for result in cls.results:
            print(result)