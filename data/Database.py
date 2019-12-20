import json
import logging
import os
import sqlite3 as lite
from collections import OrderedDict
from datetime import datetime, date

from Stock import Stock
from Transaction import Dividend, Buy, Sell, Split, Withdrawal, Deposit


class UnknownStockException(Exception):
    pass


class UnknownTransactionTypeException(Exception):
    pass


class Database:

    def __init__(self, database_path):
        self.db_path = database_path
        self.con = lite.connect(self.db_path)

    def setup(self, data_structure_path, initial_data_path):
        logging.info("Setup database")
        self._read_and_execute_sql_from_file(data_structure_path)
        self._read_and_execute_sql_from_file(initial_data_path)
        self._create_triggers()

    def _create_triggers(self):
        sql = '''
            CREATE TRIGGER %s
            BEFORE %s
            ON transactions
            WHEN NEW.stock IS NULL
            AND NEW.trans_type IN ('Deposit', 'Withdrawal')
            BEGIN
            SELECT CASE WHEN((
                SELECT 1
                FROM transactions
                WHERE stock IS NULL
                AND NEW.trans_date = trans_date AND NEW.fees = fees
                )
                NOTNULL) THEN RAISE(ABORT, "error row exists") END;
            END;'''
        cur = self.con.cursor()
        cur.execute(sql % ("UniqueColumnCheckNullInsert", "INSERT"))
        cur.execute(sql % ("UniqueColumnCheckNullUpdate", "UPDATE"))
        self.con.commit()

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
        sql = "SELECT identifier from stock_identifier WHERE stock = '%s'" % stock
        cur = self.con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        descriptions = []
        for row in rows:
            descriptions.append(row[0])
        return descriptions

    def get_prices(self, stock):
        sql = "SELECT price_date, price from prices WHERE stock = '%s'" % stock
        cur = self.con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        prices = []
        for row in rows:
            prices.append((row[0], row[1]))
        return prices

    def dividends_this_year(self, stock):
        logging.debug("Dividends received during they year")
        today = date(datetime.today().year, 1, 1).strftime("%Y-%m-%d")
        logging.debug("Today: %s" % today)
        sql = "SELECT COUNT(DISTINCT trans_date) FROM transactions WHERE trans_type = 'Dividend' AND"
        sql += " stock = '%s' AND trans_date > '%s'" % (stock, today)
        logging.debug(sql)
        cur = self.con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            return row[0]
        return 0

    def get_all_stocks(self, start_date=None, end_date=None, in_portfolio=True):
        logging.debug("Get stock information from database")
        sql = "SELECT signature, name, exchange, currency, dividend_per_year, dividend_forecast, bloomberg_signature"
        sql += " ,stock_id, stock_name, IFNULL(is_stock, 1) is_stock FROM stocks"
        sql += " LEFT OUTER JOIN stock_bloomberg ON signature=stock_bloomberg.stock"
        sql += " LEFT OUTER JOIN stock_avanza ON signature=stock_avanza.stock"
        sql += " ORDER BY name"
        logging.debug(sql)
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
            bloomberg = row[6]
            currency = row[3]
            dividend_per_year = row[4]
            dividend_forecast = row[5]

            if dividend_per_year == 0:
                dividend_per_year = row[4]

            avanza_id = row[7]
            avanza_name = row[8]
            is_stock = row[9]
            stock = Stock(signature, row[1], google, yahoo, currency, 'Aktie', self.get_descriptions(signature),
                          dividend_per_year, dividend_forecast, bloomberg, avanza_id, avanza_name, is_stock)

            transactions = self.get_transactions(signature, start_date=None, end_date=None)
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

    @staticmethod
    def get_stock_prices(signature, start_date, end_date):
        return []

    def save_price(self, stock, date, price):
        logging.debug("Saving historical price for %s" % stock)
        sql = "INSERT OR REPLACE INTO prices (stock, price_date, price) VALUES (%s, %s, %s)" % (stock, date, price)
        cur = self.con.cursor()
        cur.execute(sql)
        self.con.commit()

    def save_transactions(self, new_transactions):
        logging.debug("Saving %s new transactions" % len(new_transactions))
        for transaction in new_transactions:
            try:
                self.save_transaction(transaction)
            except UnknownStockException as e:
                logging.debug(e)
        self.con.commit()

    def save_transaction(self, transaction):
        logging.debug("Save transaction (%s)" % transaction)
        stock_key = self._get_stock_key_from_description(transaction.stock)
        split_ratio = 1.0
        if transaction.str_type == "Split":
            split_ratio = self._get_split_ratio(stock_key)
        sql = "INSERT INTO transactions (trans_date, trans_type, stock, units, price, fees, split_ratio) " \
              "VALUES (?, ?, ?, ?, ?, ?, ?)"
        cur = self.con.cursor()
        transactions = ((transaction.date.strftime("%Y-%m-%d %H:%M:%S"), transaction.str_type, stock_key,
                         transaction.units, transaction.price, transaction.amount, split_ratio),)
        logging.debug(transactions)
        try:
            cur.executemany(sql, transactions)
            logging.debug("Transaction %s saved" % transactions)
        except lite.IntegrityError as e:
            logging.debug(e)
            logging.debug(transactions)

    def _get_stock_key_from_description(self, stock_desc):
        if not stock_desc:
            return None
        sql = 'SELECT stock FROM stock_identifier WHERE identifier = "%s"' % stock_desc
        logging.debug(sql)
        cur = self.con.cursor()
        cur.execute(sql)
        stock_key = cur.fetchone()
        if not stock_key:
            raise UnknownStockException("Unknown stock description %s" % stock_desc)

        return str(stock_key[0])

    def _get_split_ratio(self, stock_key):
        sql = "SELECT ratio FROM split_ratio WHERE stock = '%s'" % stock_key
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

    def get_transactions(self, stock=None, transaction_type=None, start_date=None, end_date=None, return_json=False):
        sql = "SELECT trans_date, trans_type, stock, name, units, price, fees, split_ratio FROM transactions"
        if not stock:
            sql += " LEFT"
        sql += " JOIN stocks ON stock=signature"
        sql_operator = "WHERE"
        if transaction_type:
            sql += " %s trans_type IN (%s)" % (sql_operator, ",".join("'{0}'".format(t) for t in transaction_type))
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
                transactions.append(Sell(trans.get('stock'), trans.get('trans_date'), trans.get('price'),
                                         trans.get('units'), trans.get('fees')))
            elif trans.get('trans_type') in ('Buy', 'Transfer'):
                transactions.append(Buy(trans.get('stock'), trans.get('trans_date'), trans.get('price'),
                                        trans.get('units'), trans.get('fees')))
            elif trans.get('trans_type') == "Dividend":
                transactions.append(Dividend(trans.get('name'), trans.get('trans_date'), trans.get('price'),
                                             trans.get('units')))
            elif trans.get('trans_type') == "Split":
                transactions.append(Split(trans.get('stock'), trans.get('trans_date'), trans.get('split_ratio')))
            elif trans.get('trans_type') == "Withdrawal":
                logging.debug(trans.get('fees'))
                transactions.append(Withdrawal(trans.get('trans_date'), trans.get('fees')))
            elif trans.get('trans_type') == "Deposit":
                transactions.append(Deposit(trans.get('trans_date'), trans.get('fees')))

        return transactions

    def get_stock_name(self, signature):
        sql = "SELECT name FROM stocks WHERE signature='%s'" % signature
        return self.query_db(sql)

    def query_db(self, query, args=(), one=False):
        # type: (object, object, object) -> object
        logging.debug(query)
        cur = self.con.cursor()
        cur.execute(str(query), args)
        r = [OrderedDict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        return (r[0] if r else None) if one else r

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
