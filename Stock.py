__author__ = 'daniel'
from data.FinanceService import FinanceService, GoogleFinance, YahooFinance
from Transaction import Buy, Sell, Transfer, Split,Dividend
import logging

class Stock(object):
    def __init__(self, key, name, google_quote, yahoo_quote, currency, kind = "Aktie", descriptions = [],
                 dividend_per_year=1, dividend_forecast=0.0):
        self.key = key
        self.name = name
        self.google_quote = str(google_quote)
        self.yahoo_quote = str(yahoo_quote)
        self.currency = currency
        self.finance_service = FinanceService()
        self.google_finance = GoogleFinance()
        self.yahoo_finance = YahooFinance()
        self.transactions = []
        self.kind = kind
        self.descriptions = descriptions
        self.dividend_per_year = dividend_per_year
        self.dividend_forecast = dividend_forecast

        self.total_amount = 0
        self.total_units  = 0
        self.total_dividends = 0
        self.realized_gain = 0
        self.prices = dict()

    def get_total_price(self):
        if self.total_units == 0:
            return 0
        return self.total_amount/self.total_units

    def add_price(self, date, price):
        self.prices[date] = price

    def get_price(self, start_date=None, end_date=None):
        if start_date or end_date:
            return self.finance_service.get_historical_price(self.yahoo_quote, start_date=start_date, end_date=end_date)
        return self.finance_service.get_stock_price(self.google_quote, self.yahoo_quote)

    def has_description(self, description):
        return description in self.descriptions or self.key == description

    def gain_of_transaction(self, transaction):
        return ((transaction.amount/transaction.units)-(self.total_amount/self.total_units))*transaction.units

    def add_transaction(self, transaction):
        add_transaction = True
        if isinstance(transaction, Split):
            for trans in self.transactions:
                if trans.date == transaction.date and trans.units == transaction.units:
                    add_transaction = False
            if add_transaction and transaction.units > 0:
                logging.debug("%s" % ([self.name, self.total_amount, transaction.amount]))
                self.total_units = self.total_units * transaction.units
        elif isinstance(transaction, Dividend):
            self.total_dividends += transaction.units*transaction.price
        elif isinstance(transaction, Buy):
            self.total_units += transaction.units
            self.total_amount += transaction.amount
            logging.debug("%s" % ([self.name, type(transaction), self.total_amount, transaction.amount, self.total_units, transaction.units]))

        elif isinstance(transaction, Sell):
            logging.debug(transaction)
            self.realized_gain += self.gain_of_transaction(transaction)
            self.total_units -= transaction.units
            self.total_amount -= transaction.amount
            logging.debug("%s" % ([self.name, type(transaction), self.total_amount, transaction.amount, self.total_units, transaction.units, self.realized_gain]))

        if add_transaction:
            if self.total_units == 0:
                self.total_amount = 0
            self.transactions.append(transaction)

    def get_dividend_forecast(self):
        return self.dividend_forecast

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
        return self.total_dividends

    def calculate_transaction_average(self, transaction):
        if False and self.currency == "SEK":
            return transaction.units*transaction.price+transaction.fee
        else:
            return transaction.amount

    @staticmethod
    def to_table_header():
        return ["Name", "Price", "Currency", "Currency price"]

    def to_table(self):
        stock_price = self.finance_service.get_stock_price(self.google_quote, self.yahoo_quote)
        currency_price = self.finance_service.get_currency_price(self.currency)

        #google_price =  self.google_finance.get_stock_price(self.google_quote)
        #google_currency = "--" #self.google_finance.get_currency_price(self.currency)
        #yahoo_price = self.yahoo_finance.get_stock_price(self.yahoo_quote)
        return [self.name, stock_price, self.currency, currency_price]


