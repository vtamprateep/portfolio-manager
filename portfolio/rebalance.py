#!/Users/vtamprateep/opt/anaconda3/bin/python

from tda import auth, client, orders
from dotenv import load_dotenv
from selenium import webdriver
from collections import defaultdict
from pathlib import Path
import psycopg2
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
        path = Path(__file__).resolve().parents[1].absolute()
        path = os.path.join(path, 'chromedriver')
    return webdriver.Chrome(path)

def get_account_info(client, acc_number, fields = None):
    response = client.get_account(acc_number, fields = fields).json()
    return response

def get_stock_quote(client, symbol):
    price_quote = client.get_quote(symbol).json()
    return price_quote

def get_stock_target(cursor):
    query = '''
        SELECT symbol, target
        FROM holdings
        WHERE target > 0;
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    holdings = defaultdict(int)

    for pair in results:
        holdings[pair[0]] = pair[1]

    return holdings

def rebalance_portfolio(client, acc_bal, position, target):
    cur_val = acc_bal['liquidationValue']
    buy = defaultdict(int)
    sell = defaultdict(int)

    for item in position:
        ticker = item['instrument']['symbol']
        quantity = item['longQuantity']
        price = get_stock_quote(client, ticker)[ticker]['lastPrice']

        if ticker not in target:
            adjust = -cur_val * target[ticker] // price
        else:
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

    # Get .env variables
    TD_KEY = os.getenv('CONSUMER_KEY')
    ACC_NUMBER = os.getenv('ACC_NUMBER')
    REDIRECT_URI = os.getenv('REDIRECT_URI')
    FOLDER_PATH = Path(__file__).resolve().parents[1].absolute()
    TOKEN_PATH = os.path.join(FOLDER_PATH, 'tokens/token.pickle')
    API_KEY = TD_KEY + '@AMER.OAUTHAP'

    # Connect to securities database
    conn = psycopg2.connect("dbname=securities user=postgres")
    cur = conn.cursor()

    # Connect client and get account info
    CLIENT = connect_client(API_KEY, REDIRECT_URI, TOKEN_PATH, get_webdriver)
    acc_info = get_account_info(CLIENT, ACC_NUMBER, CLIENT.Account.Fields.POSITIONS)['securitiesAccount']
    target_holding = get_stock_target(cur)

    # Get buy, sell orders
    buy, sell = rebalance_portfolio(CLIENT, acc_info['currentBalances'], acc_info['positions'], target_holding)
    print(buy, sell)
    
    # Place orders
    place_orders(CLIENT, ACC_NUMBER, buy, sell)