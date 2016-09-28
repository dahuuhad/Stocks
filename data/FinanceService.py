__author__ = 'daniel'

import json
import logging

from googlefinance import getQuotes
from yahoo_finance import Share, Currency


class FinanceService(object):
    def __init__(self):
        self.base_url = ""
        self.base_currency = "SEK"
    def get_currency_price(self, currency):

        if currency == self.base_currency:
            return 1.0
        try:
            currency_service = Currency(currency+self.base_currency)
            return currency_service.get_rate()
        except Exception:
            return "--"

    def get_stock_price(self, google_symbol, yahoo_symbol):
        try:
            return getQuotes(google_symbol)[0].get('LastTradePrice')
        except Exception:
            logging.debug("Google Finance unknown symbol: %s" % google_symbol)
        try:
            share = Share(yahoo_symbol)
            return share.get_price()
        except Exception:
            logging.debug("Yahoo Finance unknown symbol: %s" % yahoo_symbol)

        return "--"

class GoogleFinance(FinanceService):

    def __init__(self):
        super(GoogleFinance, self).__init__()

    def get_stock_price(self, symbol):
        try:
            price = getQuotes(symbol)[0].get('LastTradePrice')
        except Exception:
            price = "--"
        return price

    def get_currency_price(self, currency):
        if currency == "SEK":
            return "1.0"
        try:
            print json.dumps(getQuotes("CURRENCY:"+currency+"SEK"), indent=2)
            price = getQuotes(currency)[0].get('LastTradePrice')
        except Exception:
            price = "--"
        return price


class YahooFinance(FinanceService):

    def __init__(self):
        super(YahooFinance, self).__init__()

    def get_currency_price(self, currency):
        raise NotImplementedError

    def get_stock_price(self, symbol):
        try:
            share = Share(symbol)
            price = share.get_price()
        except Exception:
            price = "--"
        return price

