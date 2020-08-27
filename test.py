#!/Users/vtamprateep/opt/anaconda3/bin/python

from pathlib import Path
from tda import auth, client
from dotenv import load_dotenv
from schema import Schema, And, Use, Optional, SchemaError
from portfolio import rebalance
import unittest
import os
load_dotenv()

# Constants
ROOT_DIRECTORY = Path(__file__).parent.absolute()
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

class TestPortfolioRebalance(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestPortfolioRebalance, self).__init__(*args, **kwargs)

        self.rebalance_portfolio = rebalance.rebalance_portfolio
        self.get_account_info = rebalance.get_account_info

    
    def test_rebalance_portfolio(self):
        pass

    def test_get_account_info(self):

        acc_structure = Schema(
            {
                'securitiesAccount': {
                    'type': str,
                    'accountId': str,
                    'roundTrips': int,
                    'isDayTrader': bool,
                    'isClosingOnlyRestricted': bool,
                    Optional('positions'): [
                        {
                            'shortQuantity': float,
                            'averagePrice': float,
                            'currentDayProfitLoss': float,
                            'currentDayProfitLossPercentage': float,
                            'longQuantity': float,
                            'settledLongQuantity': float,
                            'settledShortQuantity': float,
                            'instrument': {
                                'assetType': str,
                                'cusip': str,
                                'symbol': str,
                            },
                            'marketValue': float,
                            'maintenanceRequirement': float
                        },
                    ],
                    'initialBalances': {
                        'accruedInterest': float,
                        'cashAvailableForTrading': float,
                        'cashAvailableForWithdrawal': float,
                        'cashBalance': float,
                        'bondValue': float,
                        'cashReceipts': float,
                        'liquidationValue': float,
                        'longOptionMarketValue': float,
                        'longStockValue': float,
                        'moneyMarketFund': float,
                        'mutualFundValue': float,
                        'shortOptionMarketValue': float,
                        'shortStockValue': float,
                        'isInCall': bool,
                        'unsettledCash': float,
                        'cashDebitCallValue': float,
                        'pendingDeposits': float,
                        'accountValue': float
                    },
                    'currentBalances': {
                        'accruedInterest': float,
                        'cashBalance': float,
                        'cashReceipts': float,
                        'longOptionMarketValue': float,
                        'liquidationValue': float,
                        'longMarketValue': float,
                        'moneyMarketFund': float,
                        'savings': float,
                        'shortMarketValue': float,
                        'pendingDeposits': float,
                        'cashAvailableForTrading': float,
                        'cashAvailableForWithdrawal': float,
                        'cashCall': float,
                        'longNonMarginableMarketValue': float,
                        'totalCash': float,
                        'shortOptionMarketValue': float,
                        'mutualFundValue': float,
                        'bondValue': float,
                        'cashDebitCallValue': float,
                        'unsettledCash': float,
                    },
                    'projectedBalances': {
                        'cashAvailableForTrading': float,
                        'cashAvailableForWithdrawal': float,
                    }
                }
            }
        )

        acc_structure.validate(self.get_account_info(TDA_CLIENT, ACC_NUMBER))

if __name__ == '__main__':
    unittest.main()

        
    