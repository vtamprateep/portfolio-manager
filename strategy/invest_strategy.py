#!/Users/vtamprateep/opt/anaconda3/bin/python

from pathlib import Path
import pandas as pd
import psycopg2
import numpy as np
import json
import os


class MomentumStrategy:
    def __init__(self, data):
        self.HOLDINGS = dict()
        self.DATA = None

    def get_allocation(self):
        pass

class MeanRegressionStrategy:
    def __init__(self, data):
        self.HOLDINGS = dict()
        self.DATA = None

    def get_allocation(self):
        pass

class VanillaStrategy:
    def __init__(self):
        self.HOLDINGS = {
            'SPY': 0.75,
            'IWO': 0.25,
        }

    def get_allocation(self):
        return self.HOLDINGS

if __name__ == '__main__':
    # Connect db
    conn = psycopg2.connect('dbname=securities user=postgres')
    cur = conn.cursor()