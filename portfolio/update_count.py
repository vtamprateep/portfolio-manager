#!/Users/vtamprateep/opt/anaconda3/bin/python

from tda import auth, client, orders
from dotenv import load_dotenv
from selenium import webdriver
from collections import defaultdict
from pathlib import Path
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

if __name__ == '__main__':
    pass