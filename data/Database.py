import sqlite3 as lite
import sys
import logging
from Stock import Stock
from Transaction import Dividend, Buy, Sell, Split, Transfer
from datetime import datetime


class UnknownStockException(Exception):
    pass


class UnknownTransactionTypeException(Exception):
    pass


class Database():

    def __init__(self, database_path, data_structure_path, initial_data_path):
        self.db_path = database_path
        self.con = lite.connect(self.db_path)
        self._read_and_execute_sql_from_file(data_structure_path)
        self._read_and_execute_sql_from_file(initial_data_path)

    def _read_and_execute_sql_from_file(self, sql_file_path):
        logging.debug("Reading sql commands from %s" % sql_file_path)
        f = open(sql_file_path, 'r')
        sql = f.read()
        f.close()
        lite.complete_statement(sql)
        sql_commands = sql.split(';')
        for sql_command in sql_commands:
            if not sql_command:
                continue
            logging.debug("Executing: %s" % sql_command)
            cur = self.con.cursor()
            cur.execute(sql_command)
            cur.close()
        self.con.commit()

    def get_descriptions(self, stock):
        sql = "SELECT identifier from stock_identifier WHERE stock = '%s'" % (stock)
        cur = self.con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        descriptions = []
        for row in rows:
            descriptions.append(row[0])
        return descriptions

    def get_all_stocks(self):
        logging.debug("Get stock information from database")
        sql = "SELECT signature, name, exchange, currency FROM stocks"
        cur = self.con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        stocks = []
        for row in rows:
            logging.debug(row)
            signature = row[0]
            exchange = row[2]
            google = exchange + ":" + signature
            yahoo = signature + "." + signature
            stocks.append(Stock(signature, row[1], google, yahoo, row[3], 'Aktie', self.get_descriptions(signature)))
        return stocks

    def save_transactions(self, new_transactions):
        logging.info("Save transactions")
        for transaction in new_transactions:
            try:
                self.save_transaction(transaction)
            except UnknownStockException, e:
                logging.error(e)
        self.con.commit()
                
    def save_transaction(self, transaction):
        logging.info("Save transaction")
        stock_key = self._get_stock_key_from_description(transaction.stock)
        transaction_type = self._get_transaction_type(transaction)
        split_ratio = 1.0
        if transaction_type == "Split":
            split_ratio = self._get_split_ratio(stock_key)
        sql = "INSERT INTO transactions (trans_date, trans_type, stock, units, price, split_ratio) VALUES (?, ?, ?, ?, ?, ?)"
        cur = self.con.cursor()
        transactions = ((transaction.date.strftime("%Y-%m-%d %H:%M:%S"), transaction_type, stock_key, transaction.units, transaction.price, split_ratio),)
        logging.debug(transactions)
        try:
            cur.executemany(sql, transactions)
        except lite.IntegrityError, e:
            logging.error(e)

    def _get_stock_key_from_description(self, stock_desc):
        sql = 'SELECT stock FROM stock_identifier WHERE identifier = "%s"' % (stock_desc)
        logging.debug(sql)
        cur = self.con.cursor()
        cur.execute(sql)
        stock_key = cur.fetchone()
        if not stock_key:
            raise UnknownStockException("Unknown stock description %s" % stock_desc)

        return str(stock_key[0])

    def _get_transaction_type(self, transaction):
        if isinstance(transaction, Buy):
            return "Buy"
        elif isinstance(transaction, Sell):
            return "Sell"
        elif isinstance(transaction, Dividend):
            return "Dividend"
        elif isinstance(transaction, Split):
            return "Split"
        elif isinstance(transaction, Transfer):
            return "Transfer"
        else:
            raise UnknownTransactionTypeException("Unknow transaction type %s" % type(transaction))

    def _get_split_ratio(self, stock_key):
        sql = "SELECT ratio FROM split_ratio WHERE stock = '%s'" % (stock_key)
        cur = self.con.cursor()
        cur.execute(sql)
        ratio = cur.fetchone()
        if ratio:
            return ratio[0]
        return 1.0
