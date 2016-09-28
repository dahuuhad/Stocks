# -*- coding: utf-8 -*-
import os

__author__ = 'daniel'
from tabulate import tabulate

from Stock import Stock
from Transaction import Dividend, Buy, Sell, Transfer, Split



class Report(object):
    def __init__(self, report_path=None):
        self._report_path = report_path

    def setup(self):
        raise NotImplementedError

    def generate_stock_summary(self, file_name, stocks):
        raise NotImplementedError

    def generate_transaction_history(self, file_name, transactions):
        raise NotImplementedError

    def generate_dividend_summary(self, file_name, transactions):
        raise NotImplementedError

    def generate_stock_depot(self, file_name, transactions):
        raise NotImplementedError

    def generate_deposits_per_year(self, file_name, transactions):
        raise NotImplementedError

    def _save_to_file(self, file_name, text):
        """

        :rtype : object
        """
        with open(os.path.join(self._report_path, file_name), 'w') as my_file:
            #print text
            print "Write to %s" % my_file.name
            my_file.write(text.encode("latin1"))
            my_file.close()


class CSVReport(Report):
    def setup(self):
        pass

    def generate_dividend_summary(self, file_name, transactions):
        pass

    def generate_stock_summary(self, file_name, stocks):
        pass

    def generate_transaction_history(self, file_name, transactions):
        pass

class PlainReport(Report):


    def setup(self):
        raise NotImplementedError

    def generate_stock_summary(self, file_name, stocks):
        stock_table = []
        for stock in stocks:
            stock_table.append(stock.to_table())
        self._save_to_file(file_name, tabulate(stock_table, Stock.to_table_header()))

    def generate_transaction_history(self, file_name, transactions):
        transaction_table = []
        for transaction in transactions:
            transaction_table.append(transaction.to_table())
        self._save_to_file(file_name, tabulate(transaction_table, Dividend.to_table_header()))

    def generate_dividend_summary(self, file_name, transactions):
        # Generate per year
        yearly_dividends = {}
        stock_dividends = {}
        for dividend in transactions:
            year = dividend.date.year
            stock = dividend.stock
            cost = dividend.price * dividend.units
            yearly_dividends[year] = yearly_dividends.get(year, 0) + cost
            stock_dividends[stock] = stock_dividends.get(stock, 0) + cost

        stock_header = ["Stock", "Total dividends"]
        summary_data = []
        for key, value in stock_dividends.iteritems():
            summary_data.append([key, int(value)])
        self._save_to_file("dividend_stock_summary.txt", tabulate(summary_data, stock_header))

        summary_header = ["Year", "Total dividends"]
        summary_data = []
        for key, value in yearly_dividends.iteritems():
            summary_data.append([key, int(value)])
        self._save_to_file("dividend_year_summary.txt", tabulate(summary_data, summary_header))

    def generate_stock_depot(self, file_name, transactions):
        depot = {}
        for transaction in reversed(transactions):
            if isinstance(transaction, Sell):
                depot[transaction.stock] = depot.get(transaction.stock, 0) - transaction.units
            elif isinstance(transaction, Split):
                pass
            elif isinstance(transaction, Buy) or isinstance(transaction, Transfer):
                depot[transaction.stock] = depot.get(transaction.stock, 0) + transaction.units
        summary_header = ["Stock", "Units"]
        summary_data = []
        for key, value in sorted(depot.iteritems()):
            if int(value) != 0:
                summary_data.append([key, int(value)])
        self._save_to_file(file_name, tabulate(summary_data, summary_header))

    def generate_deposits_per_year(self, file_name, transactions):
        depot = {}
        for transaction in transactions:
            if isinstance(transaction, Sell):
                depot[transaction.stock] = depot.get(transaction.stock, 0) - transaction.units
            elif isinstance(transaction, Buy):
                depot[transaction.stock] = depot.get(transaction.stock, 0) + transaction.units
        summary_header = ["Stock", "Units"]
        summary_data = []
        for key, value in depot.iteritems():
            summary_data.append([key, int(value)])
        self._save_to_file(file_name, tabulate(summary_data, summary_header))


class PdfReport(Report):
    def generate_dividend_summary(self, file_name, transactions):
        pass

    def setup(self):
        raise NotImplementedError

    def generate_stock_summary(self, file_name, stocks):
        raise NotImplementedError

    def generate_transaction_history(self, file_name, transactions):
        raise NotImplementedError


class HtmlReport(Report):
    def generate_dividend_summary(self, file_name, transactions):
        pass

    def setup(self):
        raise NotImplementedError

    def generate_stock_summary(self, file_name, stocks):
        raise NotImplementedError

    def generate_transaction_history(self, file_name, transactions):
        raise NotImplementedError
