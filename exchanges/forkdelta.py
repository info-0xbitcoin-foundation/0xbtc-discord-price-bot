"""
API for ForkDelta

TODO: replace with real API instead of relying on livecoinwatch

data = 
{'data': [
  {
    '__v': 0,
    '_id': '5ae231e61bf2276634e771d5',
    'active': True,
    'base': '0xBTC',
    'exchange': 'ForkDelta',
    'last': 0.594567000066063,
    'lastq': 660.6300000000001,
    'outlier': False,
    'quote': 'ETH',
  # last price in the quote currency
    'rate': 0.0009000000001,
    'url': 'https://forkdelta.github.io/#!/trade/0xBTC-ETH',
  # value in USD
    'usd': 0.594567000066063,
  # price of the quote currency (ETH, BTC, etc) in USD
    'usdq': 660.6300000000001,
  # 24h volume in USD
    'volume': 20153.666549554204,
  # volume of this exchange as % of total volume for this coin
    'volumep': 100,
    'volumepq': 0.0007236425477855652
  },{
    # info for exchange #2, etc
  }],


"""
from .livecoinwatch import LiveCoinWatchAPI


class ForkDeltaAPI(LiveCoinWatchAPI):
    def __init__(self, currency_symbol):
        super().__init__(currency_symbol, allowed_apis=['ForkDelta'])
        self.exchange_name = "Fork Delta"
        self.command_names = ['fd', 'fork delta']
        self.short_url = "https://bit.ly/2rqTGWB"

if __name__ == "__main__":
    oxbtc_api = ForkDeltaAPI('0xBTC')
    oxbtc_api.load_once_and_print_values()

    dai_api = ForkDeltaAPI('OMG')
    dai_api.load_once_and_print_values()
