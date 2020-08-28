#!/Users/vtamprateep/opt/anaconda3/bin/python

from pathlib import Path
from tda import auth, client
from dotenv import load_dotenv
from schema import Schema, And, Use, Optional, SchemaError
import unittest
import os
import json


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

class TestTDAPI(unittest.TestCase):

    def test_account(self):
        ACC_STRUCTURE = Schema(
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
                                Optional('description'): str,
                                Optional('type'): str,
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

        response = TDA_CLIENT.get_account(ACC_NUMBER, fields = TDA_CLIENT.Account.Fields.POSITIONS).json()
        ACC_STRUCTURE.validate(response)

    def test_quotes(self):
        QUOTE_STRUCTURE = Schema({
            str: {
                "assetType": str,
                "assetMainType": str,
                "cusip": str,
                "assetSubType": str,
                "symbol": str,
                "description": str,
                "bidPrice": float,
                "bidSize": int,
                "bidId": str,
                "askPrice": float,
                "askSize": int,
                "askId": str,
                "lastPrice": float,
                "lastSize": int,
                "lastId": str,
                "openPrice": float,
                "highPrice": float,
                "lowPrice": float,
                "bidTick": str,
                "closePrice": float,
                "netChange": float,
                "totalVolume": int,
                "quoteTimeInLong": int,
                "tradeTimeInLong": int,
                "mark": float,
                "exchange": str,
                "exchangeName": str,
                "marginable": bool,
                "shortable": bool,
                "volatility": float,
                "digits": int,
                "52WkHigh": float,
                "52WkLow": float,
                "nAV": float,
                "peRatio": float,
                "divAmount": float,
                "divYield": float,
                "divDate": str,
                "securityStatus": str,
                "regularMarketLastPrice": float,
                "regularMarketLastSize": int,
                "regularMarketNetChange": float,
                "regularMarketTradeTimeInLong": int,
                "netPercentChangeInDouble": float,
                "markChangeInDouble": float,
                "markPercentChangeInDouble": float,
                "regularMarketPercentChangeInDouble": float,
                "delayed": bool
            }
        })

        test_case = ['SPY', 'IWO']

        for sym in test_case:
            response = TDA_CLIENT.get_quote(sym).json()
            QUOTE_STRUCTURE.validate(response)

if __name__ == '__main__':
    unittest.main()