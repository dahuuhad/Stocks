__author__ = 'daniel'

import logging

import requests
from bs4 import BeautifulSoup

from Transaction import Buy, Dividend, Sell, Split


def _get_fund_price(name):
    url = 'https://www.di.se/fonder/%s/' % name
    response = requests.get(url)
    if response.status_code != 200:
        return ""
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find('span', class_='js_real-time-stock-details-price').getText(strip=True)


class Stock:
    def __init__(self, key, name, currency, kind="Aktie",
                 descriptions=None, dividend_per_year=1, dividend_forecast=0.0,
                 bloomberg_quote=None, avanza_id=None,
                 avanza_name=None, is_stock=1):
        if descriptions is None:
            descriptions = []
        self.key = key
        self.name = name
        self.currency = currency
        self.bloomberg_finance = bloomberg_quote
        self.transactions = []
        self.kind = kind
        self.descriptions = descriptions
        self.dividend_per_year = dividend_per_year
        self.dividend_forecast_per_stock = dividend_forecast

        if is_stock == 1:
            self.avanza_url = f"https://www.avanza.se/aktier/om-aktien.html/{avanza_id}/" \
                              f"{avanza_name}"
            self.avanza_price = f"IMPORTXML(\"{self.avanza_url}\"; \"// span [@class='pushBox " \
                                f"roundCorners3']\")"
        elif is_stock == 0:
            logging.info(self.name)
            self.avanza_url = f"https://www.avanza.se/fonder/om-fonden.html/{avanza_id}/" \
                              f"{avanza_name}"
            self.avanza_price = _get_fund_price(self.bloomberg_finance)
        elif is_stock == 2:
            self.avanza_url = f"https://www.avanza.se/borshandlade-produkter/etf-torg/om-fonden" \
                              f".html/{avanza_id}/{avanza_name}"
            self.avanza_price = f"IMPORTXML(\"{self.avanza_url}\"; \"// span [@class='pushBox " \
                                f"roundCorners3']\")"

        self.total_amount = 0
        self.total_units = 0
        self.total_dividends = 0
        self.realized_gain = 0
        self.purchasing_sum = 0
        self.sum_of_units = 0
        self.sold_units = 0
        self.sold_sum = 0

    def get_total_price(self):
        if self.total_units == 0:
            return 0
        return self.total_amount // self.total_units

    def has_description(self, description):
        return description in self.descriptions or self.key == description

    def gain_of_transaction(self, transaction):
        return (-1 * (transaction.amount // transaction.units) -
                (self.total_amount // self.total_units)) * transaction.units * -1

    def add_transaction(self, transaction):
        add_transaction = True
        if isinstance(transaction, Split):
            for trans in self.transactions:
                if trans.date == transaction.date and trans.units == transaction.units:
                    add_transaction = False
            if add_transaction and transaction.units > 0:
                logging.debug("%s", [self.name, self.total_amount, transaction.amount])
                self.total_units = self.total_units * transaction.units
        elif isinstance(transaction, Dividend):
            self.total_dividends += transaction.units * transaction.price
        elif isinstance(transaction, Buy):
            self.total_units += transaction.units
            self.total_amount -= transaction.amount
            self.purchasing_sum -= transaction.amount
            self.sum_of_units += transaction.units
            logging.debug("%s", [self.name, transaction.str_type, self.total_amount,
                                 transaction.amount,
                                 self.total_units, transaction.units])

        elif isinstance(transaction, Sell):
            logging.debug(transaction)
            self.realized_gain += self.gain_of_transaction(transaction)
            self.total_units += transaction.units
            self.total_amount -= transaction.amount
            self.sold_units += transaction.units
            self.sold_sum -= transaction.amount
            logging.debug("%s", [self.name, transaction.str_type, self.total_amount,
                                 transaction.amount, self.total_units,
                                 transaction.units, self.realized_gain])

        if add_transaction:
            if self.total_units == 0:
                self.total_amount = 0
            self.transactions.append(transaction)

    def get_dividend_forecast(self):
        return self.dividend_forecast_per_stock

    def get_latest_dividend(self):
        dividend = 0
        latest = "2016-01-01 00:00:00"
        for trans in self.transactions:
            if not isinstance(trans, Dividend):
                continue
            if trans.date > latest:
                dividend += trans.price
        return dividend

    def get_total_dividends(self, start_date=None, end_date=None):
        if not start_date and not end_date:
            return self.total_dividends
        total_dividends = 0
        for trans in self.transactions:
            if isinstance(trans, Dividend) and start_date <= trans.date <= end_date:
                total_dividends += trans.amount
        return total_dividends

    def calculate_transaction_average(self, transaction):
        if False and self.currency == "SEK":
            return transaction.units * transaction.price + transaction.fee
        return transaction.amount
