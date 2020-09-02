import math
import scipy.stats as stats
import pandas as pd
import numpy as np
import backtrader as bt
import datetime
import psycopg2
import json
import os


class SimpleMovingAverageIndicator(bt.Indicator):
    lines = ('sma_trend',)
    params = {
        'long_ma': None,
        'short_ma': None,
    }

    def __init__(self):
        self.addminperiod(max(self.params.long_ma, self.params.short_ma))
        self.period = max(self.params.long_ma, self.params.short_ma)

    def next(self):
        sma_long = np.mean(self.data.get(size = self.long_period))
        sma_short = np.mean(self.data.get(size = self.short_period))
        self.lines.sma[0] = sma_short - sma_long


class SimpleMovingAverageStrategy(bt.Strategy):

    params = {
        'trade_freq': 9,
    }
    
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        
        self.sma = SimpleMovingAverageIndicator(long_ma = 30, short_ma = 10)
        self.days = 0
        
    def notify_order(self, order):
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
            self.bar_executed = len(self)
            
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
        self.log('Close, %.2f' % self.dataclose[0])
        if self.order:
            return
        
        if self.days > self.params.trade_freq - 1:
            self.days = 0
            if not self.position:
                if self.sma > 0:
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
            elif self.sma < 0:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

class TestEngine():
    pass

if __name__ == '__main__':
    pass