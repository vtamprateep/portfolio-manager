

import scipy.stats as stats
import pandas as pd
import numpy as np
import backtrader as bt
import datetime
import psycopg2
import json
import os


class TemplateIndicator(bt.Indicator):
    pass

# Example Simple Moving Average strategy
class TestStrategy(bt.Strategy):

    params = (
        ('maperiod30', 30),
        ('maperiod10', 10),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.days_elapsed = 0

        self.sma30 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period = self.params.maperiod30
        )
        self.sma10 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period = self.params.maperiod10
        )

    def log(self, txt, dt = None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, PRICE: %.2f, Cost: %.2f, Comm: %.2f' % (
                        order.executed.price,
                        order.executed.value,
                        order.exeuted.comm,
                    )
                )
            else:
                self.log(
                    'SELL EXECUTED, PRICE: %.2f, Cost: %.2f, Comm: %.2f' % (
                        order.executed.price,
                        order.executed.value,
                        order.exeuted.comm,
                    )
                )

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Cancelled/Margin/Rejected')
        
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

            if self.days > 4:
                self.days = 0
                
                if not self.position:
                    if self.sma10[0] > self.sma30[0]:
                        self.log('BUY CREATE, %.2f' % self.dataclose[0])
                        self.order = self.buy()
                    elif self.sma10[0] < self.sma30[0]:
                        self.log('SELL CREATE, %.2f' % self.dataclose[0])
                        self.order = self.sell()