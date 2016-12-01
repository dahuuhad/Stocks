__author__ = 'daniel'
import logging
from data.FinanceService import FinanceService, GoogleFinance, YahooFinance
from Transaction import Buy, Sell, Transfer, Split,Dividend

class Stock(object):
    def __init__(self, key, name, google_quote, yahoo_quote, currency, kind = "Aktie", descriptions = []):
        self.key = key
        self.name = name
        self.google_quote = google_quote
        self.yahoo_quote = yahoo_quote
        self.currency = currency
        self.finance_service = FinanceService()
        self.google_finance = GoogleFinance()
        self.yahoo_finance = YahooFinance()
        self.transactions = []
        self.kind = kind
        self.descriptions = descriptions

    def has_description(self, description):
        return description in self.descriptions or self.key == description

    def add_transaction(self, transaction):
        if isinstance(transaction, Split):
            for trans in self.transactions:
                if trans.date == transaction.date and trans.units == transaction.units:
                    return
        self.transactions.append(transaction)

    def get_summary(self, start_date=None, end_date=None):
        depot = {}
        for transaction in reversed(self.transactions):
            if isinstance(transaction, Sell):
                depot[transaction.stock] = depot.get(transaction.stock, 0) - transaction.units
            elif isinstance(transaction, Split):
                if transaction.units > 0:
                    depot[transaction.stock] = depot.get(transaction.stock, 0) * transaction.units
            elif isinstance(transaction, Buy) or isinstance(transaction, Transfer):
                depot[transaction.stock] = depot.get(transaction.stock, 0) + transaction.units
        summary_data = []
        for key, unit in sorted(depot.iteritems()):
            if int(unit) != 0:
                price = self.google_finance.get_stock_price(self.google_quote)
                value = 0.0
                if price != "--":
                    value = float(price)*unit
                summary_data.append([self.name, int(unit), price, value])
        return summary_data

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


