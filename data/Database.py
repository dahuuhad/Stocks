import sqlite3 as lite
import os
import json
import logging

from Stock import Stock
from Transaction import Dividend, Buy, Sell, Split, Transfer
from datetime import datetime
from collections import OrderedDict

class UnknownStockException(Exception):
    pass


class UnknownTransactionTypeException(Exception):
    pass


class Database():

    def __init__(self, database_path):
        self.db_path = database_path
        self.con = lite.connect(self.db_path)

    def setup(self, data_structure_path, initial_data_path):
        logging.info("Setup database")
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

    def get_prices(self, stock):
        sql = "SELECT price_date, price from prices WHERE stock = '%s'" % (stock)
        cur = self.con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        prices = []
        for row in rows:
            prices.append((row[0], row[1]))
        return prices

    def get_all_stocks(self, start_date=None, end_date=None, in_portfolio=True):
        logging.debug("Get stock information from database")
        sql = "SELECT signature, name, exchange, currency, dividend_per_year, dividend_forecast FROM stocks"
        sql += " ORDER BY name"
        cur = self.con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        stocks = []
        for row in rows:
            logging.debug(row)
            signature = row[0]
            exchange = row[2]
            google = exchange + ":" + signature
            yahoo = signature
            if len(exchange) == 3:
                yahoo += "." + exchange[:2]
            currency = row[3]
            dividend_per_year = row[4]
            dividend_forecast = row[5]
            stock = Stock(signature, row[1], google, yahoo, currency, 'Aktie', self.get_descriptions(signature), dividend_per_year, dividend_forecast)
            transactions = self.get_transactions(signature, start_date=start_date, end_date=end_date)
            for trans in transactions:
                stock.add_transaction(trans)
            prices = self.get_stock_prices(signature, start_date, end_date)
            for price in prices:
                stock.add_price(date=price[0], price=price[1])
            if in_portfolio and stock.total_units > 0:
                stocks.append(stock)
            elif not in_portfolio and stock.total_units == 0:
                stocks.append(stock)
        return stocks

    def get_stock_prices(self, signature, start_date, end_date):
        return []

    def save_price(self, stock, date, price):
        logging.info("Saving historical price for %s" % (stock))
        sql = "INSERT OR REPLACE INTO prices (stock, price_date, price) VALUES (%s, %s, %s)" % (stock, date, price)
        cur = self.con.cursor()
        cur.execute(sql)
        self.con.commit()

    def save_transactions(self, new_transactions):
        logging.info("Saving %s new transactions" % len(new_transactions))
        for transaction in new_transactions:
            try:
                self.save_transaction(transaction)
            except UnknownStockException, e:
                logging.error(e)
        self.con.commit()
                
    def save_transaction(self, transaction):
        logging.debug("Save transaction (%s)" % transaction)
        stock_key = self._get_stock_key_from_description(transaction.stock)
        transaction_type = self._get_transaction_type(transaction)
        split_ratio = 1.0
        if transaction_type == "Split":
            split_ratio = self._get_split_ratio(stock_key)
        sql = "INSERT INTO transactions (trans_date, trans_type, stock, units, price, fees, split_ratio) VALUES (?, ?, ?, ?, ?, ?, ?)"
        cur = self.con.cursor()
        transactions = ((transaction.date.strftime("%Y-%m-%d %H:%M:%S"), transaction_type, stock_key, transaction.units, transaction.price, transaction.amount, split_ratio),)
        logging.debug(transactions)
        try:
            cur.executemany(sql, transactions)
            logging.info("Transaction %s saved" % (transactions))
        except lite.IntegrityError, e:
            logging.error(e)
            logging.error(transactions)

    def _get_stock_key_from_description(self, stock_desc):
        sql = 'SELECT stock FROM stock_identifier WHERE identifier = "%s"' % (stock_desc.decode("latin1"))
        logging.debug(sql)
        cur = self.con.cursor()
        cur.execute(sql)
        stock_key = cur.fetchone()
        if not stock_key:
            raise UnknownStockException("Unknown stock description %s" % stock_desc)

        return str(stock_key[0])

    def _get_transaction_type(self, transaction):
        if isinstance(transaction, Sell):
            return "Sell"
        elif isinstance(transaction, Buy):
            return "Buy"
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

    def export_to_json(self, json_path):
        tables_to_export = ['transactions']
        if not os.path.isdir(json_path):
            os.mkdir(json_path)
        for table in tables_to_export:
            self.table_to_json(json_path, table)

    def table_to_json(self, json_path, table):
        with open(os.path.join(json_path, table+".json"), 'w') as file:
            data = self.get_transactions(return_json=True)

            for json_row in data:
                json_row["@timestamp"] = json_row['trans_date'].replace(" ", "T")+"Z"
                json.dump(json_row, file)
                file.write('\n')
                #json.dump(json_row, file)

    def get_transactions(self, stock=None, transaction_type=None, start_date=None, end_date=None, return_json=False):
        sql = "SELECT trans_date, trans_type, stock, name, units, price, fees, split_ratio FROM transactions"
        sql += " JOIN stocks ON stock=signature"
        sql_operator = "WHERE"
        if transaction_type:
            sql += " %s trans_type = '%s'" % (sql_operator, transaction_type)
            sql_operator = "AND"
        if stock:
            sql += " %s signature = '%s'" % (sql_operator, stock)
            sql_operator = "AND"
        if start_date:
            sql += " %s trans_date >= '%s'" % (sql_operator, start_date)
            sql_operator = "AND"
        if end_date:
            sql += " %s trans_date <= '%s'" % (sql_operator, end_date)
            sql_operator = "AND"
        sql += " ORDER BY trans_date ASC"
        result = self.query_db(sql)
        if return_json:
            return result
        transactions = []
        for trans in result:
            if trans.get('trans_type') == "Sell":
                transactions.append(Sell(trans.get('stock'), trans.get('trans_date'), trans.get('price'), trans.get('units'), trans.get('fees')))
            elif trans.get('trans_type') in ('Buy', 'Transfer'):
                transactions.append(Buy(trans.get('stock'), trans.get('trans_date'), trans.get('price'), trans.get('units'),
                                  trans.get('fees')))
            elif trans.get('trans_type') == "Dividend":
                transactions.append(Dividend(trans.get('name'), trans.get('trans_date'), trans.get('price'), trans.get('units')))
            elif trans.get('trans_type') == "Split":
                transactions.append(Split(trans.get('stock'), trans.get('trans_date'), trans.get('split_ratio')))
        return transactions

    def get_stock_name(self, signature):
        sql = "SELECT name FROM stocks WHERE signature='%s'" % signature
        return self.query_db(sql)

    def query_db(self, query, args=(), one=False):
        # type: (object, object, object) -> object
        logging.debug(query)
        cur = self.con.cursor()
        cur.execute(query, args)
        r = [OrderedDict((cur.description[i][0], value) \
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        return (r[0] if r else None) if one else r


    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
