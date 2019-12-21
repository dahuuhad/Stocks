# -*- coding: utf-8 -*-

__author__ = 'daniel'

import json
import logging

import requests
from googlefinance import getQuotes


def get_bloomberg_quote(bloomberg_symbol):
    url = "https://www.bloomberg.com/markets/chart/data/1D/%s" % bloomberg_symbol
    value = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/69.0.3497.100 Safari/537.36'
    headers = {'User-Agent': value}

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    return data["data_values"][-1][-1]


class FinanceService(object):
    def __init__(self):
        self.base_url = ""
        self.base_currency = "SEK"

    def get_stock_price(self, google_symbol, yahoo_symbol, bloomberg_symbol=None):
        if bloomberg_symbol:
            try:
                logging.info("Getting quotes for %s" % bloomberg_symbol)
                return get_bloomberg_quote(bloomberg_symbol=bloomberg_symbol)
            except Exception:
                logging.error("Bloomberg unknown symbol: %s" % bloomberg_symbol)

        try:
            logging.info("Getting quotes for %s" % google_symbol)
            quote = getQuotes(google_symbol)
            logging.debug("%s" % quote)
            return quote[0].get('LastTradePrice')
        except Exception:
            logging.debug("Google Finance unknown symbol: %s" % google_symbol)

        logging.debug("No stock price found for symbol: %s" % google_symbol)
        return "--"

    def get_currency_price(self, currency):
        pass
