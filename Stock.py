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

        self.total_amount = 0
        self.total_units  = 0
        self.total_dividends = 0

    def has_description(self, description):
        return description in self.descriptions or self.key == description

    def add_transaction(self, transaction):
        add_transaction = True
        if isinstance(transaction, Split):
            for trans in self.transactions:
                if trans.date == transaction.date and trans.units == transaction.units:
                    add_transaction = False
            if add_transaction and transaction.units > 0:
                print self.name, self.total_amount, transaction.amount
                self.total_units = self.total_units * transaction.units
        elif isinstance(transaction, Dividend):
            self.total_dividends += transaction.units*transaction.price
        elif isinstance(transaction, Buy):
            self.total_units += transaction.units
            self.total_amount += transaction.amount
            print self.name, self.total_amount, transaction.amount

        elif isinstance(transaction, Sell):
            self.total_units -= transaction.units
            self.total_amount -= transaction.amount
            print self.name, self.total_amount, -transaction.amount

        if add_transaction:
            if self.total_units == 0:
                self.total_amount = 0
            self.transactions.append(transaction)

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

    def get_summary(self, start_date=None, end_date=None):
        depot = {}
        value = 0
        no_of_transactions = 0
        for transaction in reversed(self.transactions):
            if isinstance(transaction, Dividend):
                continue
            print transaction, self.currency
            if isinstance(transaction, Sell):
                depot[transaction.stock] = depot.get(transaction.stock, 0) - transaction.units
                value -= self.calculate_transaction_average(transaction)
                no_of_transactions += 1
            elif isinstance(transaction, Split):
                if transaction.units > 0:
                    depot[transaction.stock] = depot.get(transaction.stock, 0) * transaction.units
            elif isinstance(transaction, Buy) or isinstance(transaction, Transfer):
                depot[transaction.stock] = depot.get(transaction.stock, 0) + transaction.units
                value += self.calculate_transaction_average(transaction)
                no_of_transactions += 1
        print "Depot = %s" % depot
        print "Value = %s" % (value)
        print "No of transactions = %s" % no_of_transactions
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


