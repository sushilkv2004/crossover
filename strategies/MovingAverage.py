import math
import backtrader as bt


class MovingAverage(bt.Strategy):

    results = []
    #max_roi = 0
    #max_fast = 0
    #max_slow = 0

    params = (('fast', 13),
              ('slow', 26),
              ('order_pct', .95),
              ('ticker', 'AMZN'))

    def __init__(self):
        self.fastma = bt.indicators.ExponentialMovingAverage(
            self.data.close, 
            period=self.p.fast, 
            plotname='13 day'
        )

        self.slowma = bt.indicators.ExponentialMovingAverage(
            self.data.close, 
            period=self.p.slow, 
            plotname='26 day'
        )

        self.crossover = bt.indicators.CrossOver(
            self.fastma, 
            self.slowma
        )
        self.size = 0
        self.roi = 0

    def start(self):
            self.val_start = self.broker.get_cash()  # keep the starting cash
            self.first_trade = True

    def next(self):
        if self.position.size == 0:
            #if self.fastma > self.slowma:
            if self.crossover > 0:
                amount_to_invest = (self.p.order_pct * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)
                if  self.first_trade:
                    print("Frist:",  self.PriceDateTime, self.fastma, self.slowma, self.crossover)
                    self.first_trade = False

                print("Buy {} shares of {} at {} diff {}".format(self.size, self.p.ticker, self.data.close[0],  self.fastma - self.slowma))
                self.buy(size=self.size)
            
        if self.position.size > 0:
            #if self.fastma < self.slowma:
            if self.crossover < 0:
                print("Sell {} shares of {} at {} diff {}".format(self.size, self.p.ticker, self.data.close[0], self.fastma - self.slowma))
                self.close()

    def stop(self):
        # calculate the actual returns
        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        print('{}-{}:'.format(self.params.fast, self.params.slow), end="")

        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        print('Strt = {} End={}'.format(self.val_start, self.broker.get_value()))

        print(' ROI:        {:.2f}%'.format(100.0 * self.roi))

        MovingAverage.results.append((self.params.fast, self.params.slow, round(100.0 * self.roi, 2)))

    @classmethod
    def show_max(cls):
        #print("BEST: {}-{} : {:.2f}%".format(cls.max_fast, cls.max_slow, 100.0 * cls.max_roi)
        #print(sorted(cls.max_res, key=cls.max_res[]))
        print("*"*20)
        cls.results.sort(key=lambda x: x[2], reverse=True)
        for result in cls.results:
            print(result)
        print("*"*20)

        return cls.results[0]