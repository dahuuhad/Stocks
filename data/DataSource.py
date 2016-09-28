# -*- coding: utf-8 -*-
__author__ = 'daniel'

import os
import csv

from Transaction import Dividend
from Stock import Stock
from parser.Parser import AvanzaTransactionParser


class DataSource(object):
    def __init__(self):
        self.stocks = []
        self.transactions = []

    def add_stock(self, stock):
        self.stocks.append(stock)

    def add_transaction(self, transaction):
        #print "Add transaction %s (%s)" % (type(transaction), transaction.stock)
        self.transactions.append(transaction)

    def get_stocks(self):
        return self.stocks

    def get_transactions(self, transaction_type="all"):
        if transaction_type == "all":
            return self.transactions
        elif transaction_type == "dividend":
            transactions = []
            for transaction in self.transactions:
                if isinstance(transaction, Dividend):
                    transactions.append(transaction)
            return transactions


class CvsDataSource(DataSource):
    def __init__(self, root_path="", transaction_path="transactions", stock_definition_file="Stocks.txt"):
        super(CvsDataSource, self).__init__()
        self.root_path = root_path
        self.transaction_path = None
        if root_path and transaction_path:
            self.transaction_path = os.path.join(self.root_path, transaction_path)
        self.stock_definition_file = stock_definition_file
        self._read_stocks()
        self._read_transactions()

    def _read_stocks(self):
        with open(os.path.join(self.root_path, self.stock_definition_file), 'r') as f:
            reader = csv.reader(f, dialect='excel', delimiter=';')
            for row in reader:
                self.add_stock(Stock(*row))

    def _is_csv_file(self, file_path):
        file_name, extension = os.path.splitext(file_path)
        return extension == ".csv"


    def _read_transactions(self):
        transaction_parser = AvanzaTransactionParser()
        for file_name in os.listdir(self.transaction_path):
            if self._is_csv_file(os.path.join(self.transaction_path, file_name)):
                print "Parsing %s" % file_name
                with open(os.path.join(self.transaction_path, file_name), 'r') as f:
                    reader = csv.reader(f, dialect='excel', delimiter=';')
                    for row in reader:
                        transaction = transaction_parser.parse_row(*row)
                        if transaction is not None:
                            self.add_transaction(transaction)




