# -*- coding: utf-8 -*-

__author__ = 'daniel'

import json
import logging

import requests
from googlefinance import getQuotes


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

    def get_historical_price(self, yahoo_symbol, start_date, end_date):
        try:
            logging.debug("Getting quotes for %s between %s and %s" % (yahoo_symbol, start_date, end_date))
            share = Share(yahoo_symbol)
            price = share.get_historical(start_date, end_date)
            logging.debug("Historical price is %s"  % price)
            if price:
                return float(price[0].get('Close'))
        except Exception:
            logging.debug("Yahoo Finance unknown symbol: %s" % yahoo_symbol)

    def get_stock_price(self, google_symbol, yahoo_symbol, bloomberg_symbol=None):
        if bloomberg_symbol:
            try:
                logging.debug("Getting quotes for %s" % bloomberg_symbol)
                return self.get_bloomberg_quote(bloomberg_symbol=bloomberg_symbol)
            except Exception:
                logging.error("Bloomberg unknown symbol: %s" % bloomberg_symbol)

        try:
            logging.debug("Getting quotes for %s" % google_symbol)
            quote = getQuotes(google_symbol)
            logging.debug("%s" % quote)
            return quote[0].get('LastTradePrice')
        except Exception:
            logging.debug("Google Finance unknown symbol: %s" % google_symbol)

        try:
            logging.debug("Getting quotes for %s" % yahoo_symbol)
            share = Share(yahoo_symbol)
            price = share.get_price()
            if price:
                return price
        except Exception:
            logging.debug("Yahoo Finance unknown symbol: %s" % yahoo_symbol)


        logging.debug("No stock price found for symbol: %s" % (google_symbol))
        return "--"

    def get_bloomberg_quote(self, bloomberg_symbol):
        url = "https://www.bloomberg.com/markets/chart/data/1D/%s" % bloomberg_symbol
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        return data["data_values"][-1][-1]

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


class AvanzaFinance(FinanceService):
    #=IMPORTXML("https://www.avanza.se/fonder/om-fonden.html/878733/avanza-global"; "// div [@class='SText bold']")
    # =IMPORTXML("https://www.avanza.se/aktier/om-aktien.html/13477/kopparbergs-b"; "// span [@class='pushBox roundCorners3']")
    def __init__(self):
        super(AvanzaFinance, self).__init__()

    def get_currency_price(self, currency):
        raise NotImplementedError

    def get_stock_price(self, symbol):
        try:
            share = Share(symbol)
            price = share.get_price()
        except Exception:
            price = "--"
        return price
