import math
import scipy.stats as stats
import pandas as pd
import numpy as np
import backtrader as bt
import datetime
import psycopg2
import json
import os


class TemplateStrategy(bt.Strategy):

    params = {
        'trade_freq': None,
        'indicator': None,
        'datafeed_name': None,
    }
        
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.days = 0
        
        self.inds = dict()
        for i, d in enumerate(self.datas):
            self.inds[d] = dict()
            self.inds[d]['sma'] = self.params.indicator()
        

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, PRICE: %.2f, Cost: %.2f' % (
                        order.executed.price,
                        order.executed.value,
                    )
                )
            else:
                self.log(
                    'SELL EXECUTED, Price: %.2f, Cost: %.2f' % (
                        order.executed.price,
                        order.executed.value,
                    )
                )
            self.bar_executed = len(self)

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
        
        if self.days > self.params.trade_freq - 1:
            self.days = 0
            for i, d in enumerate(self.datas):
                if self.inds[d]['sma'][0] > 0:
                    self.log('BUY CREATE, %.2f' % d.close[0])
                    self.order = self.buy(data = d, size = 2)
                else:
                    self.log('SELL CREATE, %.2f' % d.close[0])
                    self.order = self.sell(data = d, size = 2)

class SimpleMovingAverageIndicator(bt.Indicator):
    lines = ('sma_trend',)
    params = {
        'long_ma': 30,
        'short_ma': 10,
    }

    def __init__(self):
        self.addminperiod(max(self.params.long_ma, self.params.short_ma))
        self.long_period = max(self.params.long_ma, self.params.short_ma)
        self.short_period = min(self.params.long_ma, self.params.short_ma)

    def next(self):
        sma_long = np.mean(self.data.get(size = self.long_period))
        sma_short = np.mean(self.data.get(size = self.short_period))
        self.lines.sma_trend[0] = sma_short - sma_long
        

if __name__ == '__main__':
    # Connect db
    conn = psycopg2.connect('dbname=securities user=postgres')
    cur = conn.cursor()

    # Query and format data
    cur.execute('SELECT * FROM prices ORDER BY datetime ASC')
    data = pd.DataFrame(cur.fetchall(), columns = ['symbol', 'date', 'open', 'high', 'low', 'close'])
    data.loc[:, 'date'] = pd.to_datetime(data['date'])
    data = data.set_index('date')

    # Create backtest engine and add data/strategies
    cerebro = bt.Cerebro()
    
    ticker_list = data.symbol.unique()
    for ticker in ['SPY', 'IWO']: # Change to `ticker_list` when done testing
        ticker_df = data[data['symbol'] == ticker]
        cerebro.adddata(bt.feeds.PandasData(dataname = ticker_df, datetime = -1))
    
    cerebro_data = bt.feeds.PandasData(dataname = data, datetime = -1)
    cerebro.addstrategy(TemplateStrategy, trade_freq = 10, indicator = SimpleMovingAverageIndicator, datafeed_name = ticker_list)

    # Run backtest and evaluate strategies
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Close database connections
    cur.close()
    conn.close()