import invest_strategy
import math
import scipy.stats as stats
import pandas as pd
import numpy as np
import backtrader as bt
import datetime
import psycopg2
import json
import os


class TemplateIndicator(bt.Indicator):
    lines = ('test_strategy',)

    # Pass arguments as normal to params
    params = dict(
        algo_fn = None,
        period = None,
    )

    def __init__(self, sig_func = None):
        self.addminperiod(self.params.period)
        self._strat_fn = self.params.algo_fn

    def next(self):
        self.lines.test_strategy[0] = self._strat_fn(self.data.get(size = self.params.period))

class TemplateStrategy(bt.Strategy):

    params = dict(
        test_indicator = None,
        trade_freq = None,
    )
    
    def __init__(self):
        self.data_close = self.datas[0].close
        self.trade_freq = self.params.trade_freq or 1 # Default to daily
        self.days = 0

        self.order = None
        self.buyprice = None
        self.test_indicator = test_indicator

    def log(self, text, dt = None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), text))

    def notify_order(self, order):

        # Prevent additional orders if exist outstanding
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, PRICE: %.2f, Cost: %.2f, Comm %.2f' % (
                        order.executed.price,
                        order.executed.value,
                        order.executed.comm,
                    )
                )
            else:
                self.log(
                    'SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' % (
                        order.executed.price,
                        order.executed.value,
                        order.executed.comm,
                    )
                )

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        
        self.log(
            'OPERATION PROFIT, GROSS %.2f, NET %.2f' % (
                trade.pnl,
                trade.pnlcomm,
            )
        )

    def next(self):
        self.days += 1

        if self.order:
            return

        if self.days > self.trade_freq:
            self.days = 0

            if not self.position:

                if self.test_indicator[0]:
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()

            else:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

class TestEngine():
    pass

if __name__ == '__main__':
    pass