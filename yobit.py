# API For Yobit exchange
#
# Thanks SEDO devs https://github.com/CryptoProjectDev/sedo-information-discord-bot/

import time
import logging
import socket
try:
    from urllib.request import urlopen, Request
except:
    from urllib import urlopen, Request

from urllib.error import URLError

import json

import pprint

from weighted_average import WeightedAverage


class YobitAPI():
    def __init__(self, currency_symbol):
        self._SERVER_URL = "https://yobit.io/api/3/ticker"
        self.exchange_name = "Yobit"
        self.command_names = ["yobit"]
        self.last_updated_time = 0
        self.update_failure_count = 0

        self.currency_symbol = currency_symbol
        if currency_symbol == "SEDO":
            self.short_url = "https://bit.ly/2R0FHSf"
            self._currency_name_on_exchange = "sedo"
        else:
            raise RuntimeError("Unknown currency {}; need to edit yobit.py".format(currency_symbol))

        self.price_eth = None
        self.price_usd = None
        self.price_btc = None
        self.volume_usd = None
        self.volume_eth = None
        self.volume_btc = None
        self.change_24h = None
        self.eth_price_usd = None
        self.btc_price_usd = None

    def _update(self, timeout=10.0):
        method = "/{0}_btc-{0}_eth-eth_usd-btc_usd".format(self._currency_name_on_exchange)

        req = Request(
            self._SERVER_URL+method, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )

        response = urlopen(req, timeout=timeout)
        response = response.read().decode("utf-8") 
        try:
            data = json.loads(response)
        except json.decoder.JSONDecodeError:
            raise TimeoutError("bad reply from server ({})".format(repr(response)))

        volume_usd = 0

        self.price_btc = float(data['{}_btc'.format(self._currency_name_on_exchange)]['last'])
        self.volume_btc = float(data['{}_btc'.format(self._currency_name_on_exchange)]['vol'])
        self.price_eth = float(data['{}_eth'.format(self._currency_name_on_exchange)]['last'])
        self.volume_eth = float(data['{}_eth'.format(self._currency_name_on_exchange)]['vol'])
        self.eth_price_usd = float(data['eth_usd']['last'])
        self.btc_price_usd = float(data['btc_usd']['last'])

    def update(self, timeout=10.0):
        try:
            self._update(timeout=timeout)
        except (TimeoutError,
                ConnectionResetError,
                ConnectionRefusedError,
                socket.timeout,
                socket.gaierror,
                URLError) as e:
            #logging.warning('api timeout {}: {}'.format(self.exchange_name, str(e)))
            raise TimeoutError(str(e)) from e
            self.update_failure_count += 1
        else:
            self.last_updated_time = time.time()
            self.update_failure_count = 0

    def print_all_values(self):
        print(self.exchange_name, self.currency_symbol, 'price_eth    ', repr(self.price_eth))
        print(self.exchange_name, self.currency_symbol, 'price_usd    ', repr(self.price_usd))
        print(self.exchange_name, self.currency_symbol, 'price_btc    ', repr(self.price_btc))
        print(self.exchange_name, self.currency_symbol, 'volume_usd   ', repr(self.volume_usd))
        print(self.exchange_name, self.currency_symbol, 'volume_eth   ', repr(self.volume_eth))
        print(self.exchange_name, self.currency_symbol, 'volume_btc   ', repr(self.volume_btc))
        print(self.exchange_name, self.currency_symbol, 'change_24h   ', repr(self.change_24h))
        print(self.exchange_name, self.currency_symbol, 'eth_price_usd', repr(self.eth_price_usd))
        print(self.exchange_name, self.currency_symbol, 'btc_price_usd', repr(self.btc_price_usd))

if __name__ == "__main__":

    sedo_api = YobitAPI('SEDO')
    sedo_api.update()
    sedo_api.print_all_values()