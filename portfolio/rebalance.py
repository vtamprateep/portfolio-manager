#!/Users/vtamprateep/opt/anaconda3/bin/python

from tda import auth, client, orders
from dotenv import load_dotenv
from selenium import webdriver
from collections import defaultdict
from pathlib import Path
import requests
import json
import os


def connect_client(api_key, redirect_uri, token_path, webdriver_func):
    client = auth.easy_client(
        api_key = api_key,
        redirect_uri = REDIRECT_URI,
        token_path = TOKEN_PATH,
        webdriver_func = webdriver_func,
    )
    return client

def get_webdriver(path = None):
    if not path:
        path = Path(__file__).parents[1].absolute()
        path = os.path.join(path, 'chromedriver')
    return webdriver.Chrome(path)

def get_account_info(client, acc_number, fields = None):
    response = client.get_account(acc_number, fields = fields).json()
    return response

def rebalance_portfolio(acc_bal, position, target):
    cur_val = acc_bal['liquidationValue']
    buy = defaultdict(int)
    sell = defaultdict(int)

    for item in position:
        ticker = item['instrument']['symbol']
        quantity = item['longQuantity']
        price = item['marketValue'] / quantity

        if ticker not in target:
            continue

        adjust = cur_val * target[ticker] // price - quantity

        if adjust < 0:
            sell[ticker] = abs(adjust)
        elif adjust > 0:
            buy[ticker] = abs(adjust)

    return buy, sell

def place_orders(client, account_id, buy, sell):
    for key, value in sell.items():
        client.place_order(
            account_id,
            orders.equities.equity_sell_market(key, value),
        )

    for key, value in buy.items():
        client.place_order(
            account_id,
            orders.equities.equity_buy_market(key, value),
        )
    return

if __name__ == '__main__':
    load_dotenv()
    target_holding = {
        'SPY': 0.75,
        'IWO': 0.25,
    }

    # Get .env variables
    TD_KEY = os.getenv('CONSUMER_KEY')
    ACC_NUMBER = os.getenv('ACC_NUMBER')
    REDIRECT_URI = os.getenv('REDIRECT_URI')
    FOLDER_PATH = Path(__file__).parents[1].absolute()
    TOKEN_PATH = os.path.join(FOLDER_PATH, 'tokens/token.pickle')
    API_KEY = TD_KEY + '@AMER.OAUTHAP'

    # Connect client and get account info
    client = connect_client(API_KEY, REDIRECT_URI, TOKEN_PATH, get_webdriver)
    acc_info = get_account_info(client, ACC_NUMBER, client.Account.Fields.POSITIONS)['securitiesAccount']

    # Get buy, sell orders
    buy, sell = rebalance_portfolio(acc_info['currentBalances'], acc_info['positions'], target_holding)

    # Place orders
    #place_orders(client, ACC_NUMBER, buy, sell)