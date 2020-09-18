import math
import backtrader as bt


class AdxMacd(bt.Strategy):

    results = []

    params = (('fast', 12),
              ('slow', 26),
              ('macdsig', 9),
              ('order_pct', .95),
              ('ticker', 'AMZN'))

    def __init__(self):
        self.adx = bt.talib.ADX(self.data.high, self.data.low, self.data.close)

        self.plus_di = bt.talib.PLUS_DI(self.data.high, self.data.low, self.data.close)

        self.minus_di = bt.talib.MINUS_DI(self.data.high, self.data.low, self.data.close)

        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=self.p.fast,
                                       period_me2=self.p.slow,
                                       period_signal=self.p.macdsig)
        self.size = 0
        self.roi = 0
        self.trade_count = 0

    def start(self):
            self.val_start = self.broker.get_cash()  # keep the starting cash
            self.first_trade = True

    def next(self):
        if self.position.size == 0:
            if self.adx > 15 and self.adx > self.minus_di and self.plus_di > self.minus_di \
                    and self.macd.macd > self.macd.signal:

                amount_to_invest = (self.p.order_pct * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)
                if  self.first_trade:
                    #print("Frist:",  self.PriceDateTime, self.fastma, self.slowma, self.crossover)
                    self.first_trade = False
                #print("Buy  at {} total = {}".format(self.data.close[0], self.broker.get_value()))
                self.buy(size=self.size)
                self.trade_count += 1

            
        if self.position.size > 0:
            if self.plus_di <  self.minus_di and self.macd.macd < self.macd.signal:
                #print("Sell at {} total = {}".format(self.data.close[0], self.broker.get_value()))
                self.close()

    def stop(self):
        # calculate the actual returns
        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        #print('{}-{}:'.format(self.params.fast, self.params.slow), end="")

        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        print('  Strt={} End={} Traded={} ROI={:.2f}%'.format(self.val_start, self.broker.get_value(),
                                                                self.trade_count, 100.0 * self.roi))
        AdxMacd.results.append((self.params.fast, self.params.slow, round(100.0 * self.roi, 2)))

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