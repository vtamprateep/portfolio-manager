from tda import auth, client
from dotenv import load_dotenv
from selenium import webdriver
import psycopg2
import requests
import json
import os


class ConnectDB:
    def __init__(self, db_name, db_user):
        self.connection = psycopg2.connect('dbname={db_name} user={db_user}'.format(db_name = db_name, db_user = db_user))
        self.cursor = self.connection.cursor()

    def execute(self, query, args):
        self.cursor.execute(query, args)
        return

    def close(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        return

def get_webdriver(path = './chromedriver'):
    from selenium import webdriver
    return webdriver.Chrome(path)

def load_client(api_key, redirect_uri, token_path, webdriver_func):
    client = auth.easy_client(
        api_key = api_key,
        redirect_uri = redirect_uri,
        token_path = token_path,
        webdriver_func = webdriver_func,
    )
    return client

def get_account_info(client, acc_number, fields = None):
    response = client.get_account(acc_number, fields = fields).json()
    cur_balances = response['securitiesAccount']['currentBalances']
    acc_val, cash_val = cur_balances['liquidationValue'], cur_balances['cashAvailableForTrading']
    return (acc_val, cash_val)


if __name__ == '__main__':

    # Get .env variables
    load_dotenv()
    td_consumer_key = os.getenv('CONSUMER_KEY')
    acc_number = os.getenv('ACC_NUMBER')

    token_path = './token.pickle'
    api_key = td_consumer_key + '@AMER.OAUTHAP'
    redirect_uri = 'https://localhost'

    # Connect client and get account info
    client = load_client(api_key, redirect_uri, token_path, get_webdriver)
    update_val = get_account_info(client, acc_number)

    # Create connection object class
    connectDB = ConnectDB('postgres', 'postgres')
    connectDB.execute('UPDATE account SET (acc_value, cash_bal) = (%s, %s);', update_val)
    connectDB.close()