import backtrader as bt

class BuyHold(bt.Strategy):

    def start(self):
        self.size = 0
        self.roi = 0
        self.trade_count = 0

        self.val_start = self.broker.get_cash()  # keep the starting cash

    def nextstart(self):
        #print("next start")
        #print(self.broker.get_cash())

        # Buy all the available cash
        #print(self.broker.get_cash())
        size = int(self.broker.get_cash() / self.data)
        self.buy(size=size)
        #print('Bought = {}'.format(size))
        self.trade_count += 1

    def next(self):
        #print("next")
        #print(self.broker.get_cash())
        pass

    def stop(self):
        # calculate the actual returns
        self.close()
        #print('Sold')

        #print(self.broker.get_cash())
        #print(self.broker.get_value(), self.val_start)

        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        print('  Strt={} End={} Traded={} ROI={:.2f}%'.format(self.val_start, self.broker.get_value(),
                                                                self.trade_count, 100.0 * self.roi))