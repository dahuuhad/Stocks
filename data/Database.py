import sqlite3 as lite
import sys
import logging
from Stock import Stock


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