#!/Users/vtamprateep/opt/anaconda3/bin/python

from portfolio import rebalance
from dotenv import load_dotenv
from tda import auth, client
from pathlib import Path
import unittest
import os

# Constants
ROOT_DIRECTORY = Path(__file__).parents[1].absolute()
load_dotenv()

TD_KEY = os.getenv('CONSUMER_KEY')
ACC_NUMBER = os.getenv('ACC_NUMBER')
REDIRECT_URI = os.getenv('REDIRECT_URI')
TOKEN_PATH = os.path.join(ROOT_DIRECTORY, 'tokens/token.pickle')
API_KEY = TD_KEY + '@AMER.OAUTHAP'

# TDA Client
TDA_CLIENT = auth.easy_client(
    api_key = API_KEY,
    redirect_uri = REDIRECT_URI,
    token_path = TOKEN_PATH,
)

class TestAccount(unittest.TestCase):

    def test_get_account_info(self):
        response = rebalance.get_account_info(TDA_CLIENT, ACC_NUMBER)
        self.assertIsInstance(response, dict)

    def test_rebalance_portfolio(self):
        test_acc_bal = {'liquidationValue': 10000}
        
        test_position = [
            {
                'instrument': {'symbol': 'SPY'},
                'longQuantity': 10,
                'marketValue': 5000,
            },
            {
                'instrument': {'symbol': 'IWO'},
                'longQuantity': 5,
                'marketValue': 1500,
            }
        ]

        test_target = {
            'SPY': 0.75,
            'IWO': 0.25,
        }

        test_buy, test_sell = rebalance.rebalance_portfolio(test_acc_bal, test_position, test_target)
        self.assertDictEqual(test_buy, {'SPY': 5, 'IWO':3})
        self.assertDictEqual(test_sell, {})

if __name__ == '__main__':
    unittest.main()