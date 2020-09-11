# -*- coding: utf-8 -*-
__author__ = 'daniel'

import csv
import logging
import os

from parser.Parser import AvanzaTransactionParser
from stock import Stock
from Transaction import Dividend


class DataSource(object):
    def __init__(self):
        self.stocks = []
        self.transactions = []

    def add_stock(self, stock):
        self.stocks.append(stock)

    def add_transaction(self, transaction):
        logging.debug("Add transaction %s (%s)" % (type(transaction), transaction.stock))
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
        else:
            return None


def _is_csv_file(file_path):
    file_name, extension = os.path.splitext(file_path)
    return extension == ".csv"


class CvsDataSource(DataSource):
    def __init__(self, root_path="", transaction_path="transactions",
                 stock_definition_file="Stocks.txt"):
        super(CvsDataSource, self).__init__()
        self.root_path = root_path
        self.transaction_path = None
        if root_path and transaction_path:
            self.transaction_path = os.path.join(self.root_path, transaction_path)
        self.stock_definition_file = stock_definition_file
        self._read_stocks()
        self._read_transactions()

    def _read_stocks(self):
        with open(os.path.join(self.root_path, self.stock_definition_file), 'r') as csv_file:
            reader = csv.reader(csv_file, dialect='excel', delimiter=';')
            for row in reader:
                self.add_stock(Stock(*row))

    def _read_transactions(self):
        transaction_parser = AvanzaTransactionParser()
        for file_name in os.listdir(self.transaction_path):
            if _is_csv_file(os.path.join(self.transaction_path, file_name)):
                logging.info("Parsing %s" % file_name)
                with open(os.path.join(self.transaction_path, file_name), 'r') as csv_file:
                    reader = csv.reader(csv_file, dialect='excel', delimiter=';')
                    for row in reader:
                        transaction = transaction_parser.parse_row(*row)
                        if transaction is not None:
                            self.add_transaction(transaction)
