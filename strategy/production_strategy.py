#!/Users/vtamprateep/opt/anaconda3/bin/python

from pathlib import Path
import backtrader as bt
import pandas as pd
import psycopg2
import numpy as np
import json
import os


class SimpleMovingAverage:
    def __init__(self, cursor):
        self.sma_30 = None
        self.sma_10 = None
        self.QUERY = (
            '''
            SELECT *
            FROM prices
            ORDER BY symbol ASC, datetime ASC;
            '''
        )

    def get_signal(self, data):
        result_dict = dict()

        for name, group in data.groupby('symbol'):
            self.sma_30 = np.mean(group.tail(30)['close'])
            self.sma_10 = np.mean(group.tail(10)['close'])
            result_dict[name] = self.sma_10 - self.sma_30

        return result_dict

def get_data(cursor, query):
    cursor.execute(query)
    return pd.DataFrame(cursor.fetchall(), columns = ['symbol', 'date', 'open', 'high', 'low', 'close'])


if __name__ == '__main__':
    # Connect db
    conn = psycopg2.connect('dbname=securities user=postgres')
    cur = conn.cursor()

    simple_strategy = SimpleMovingAverage(cur)
    data = get_data(cur, simple_strategy.QUERY)

    cur.close()
    conn.close()