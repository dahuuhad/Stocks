__author__ = 'daniel'

import csv
import os
import sys
import logging
from operator import itemgetter
from data.DataSource import CvsDataSource
from parser.Parser import AvanzaTransactionParser
from reports.Report import PlainReport
from tabulate import tabulate
from Stock import Stock
from data.Database import Database

def setup_logging(level, logfile):
    logging.basicConfig( format='%(asctime)s %(levelname)s %(module)s::%(funcName)s (%(lineno)d) - %(message)s', level=level, filename=logfile, filemode='w')



def compare_files(file1, file2):
    import filecmp
    return filecmp.cmp(file1, file2)


root_path = os.path.join(os.sep, "Users", "daniel", "Documents", "Aktier")
stock_file = "Stocks.txt"
path_to_cvs_files = "transactions"
report_path = "reports"


def find_stock_for_transaction(stocks, transaction):
    for stock in stocks:
        if stock.has_description(transaction.stock.decode("latin1")):
            return stock
    return None


def read_transaction_rows_from_file(transaction_path):
    transactions = []
    transaction_parser = AvanzaTransactionParser()
    if not os.path.isdir(transaction_path):
        raise Exception("Directory does not exists %s" % transaction_path)
    for file_name in sorted(os.listdir(transaction_path)):
        if os.path.splitext(file_name)[1] == ".csv":
            logging.info("Parsing %s" % file_name)
            with open(os.path.join(transaction_path, file_name), 'r') as f:
                reader = csv.reader(f, dialect='excel', delimiter=';')
                for row in reader:
                    transaction = transaction_parser.parse_row(*row)
                    if transaction:
                        transactions.append(transaction)
    return transactions

def print_stock_summary(stocks):
    logging.info("Printing stock summary")
    summary_header = ["Stock", "Units", "Price", "Value"]
    summary_data = []
    for stock in stocks:
        summary_data  = summary_data + stock.get_summary()
    print tabulate(sorted(summary_data, key=itemgetter(0)), summary_header)

def main():
    db = Database('data/stocks.db', 'data/structures.sql', 'data/initial_data.sql')

    new_transactions = read_transaction_rows_from_file(os.path.join(root_path, path_to_cvs_files))
    db.save_transactions(new_transactions)
    stocks = db.get_all_stocks()
    print_stock_summary(stocks)

if __name__ == "__main__":
    setup_logging(level=logging.DEBUG, logfile="/tmp/stocks.log")
    main()
    sys.exit(0)