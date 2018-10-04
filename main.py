__author__ = 'daniel'

import csv
import os
import sys
import logging
import argparse
from operator import itemgetter
from data.DataSource import CvsDataSource
from parser.Parser import AvanzaTransactionParser
from tabulate import tabulate
from Stock import Stock
from data.Database import Database
from spreadsheet.GoogleSheet import GoogleSheet
try:
    from oauth2client import tools
except:
    pass
from datetime import datetime

parser = argparse.ArgumentParser("Read stock information from Avanza and create a Google Sheet",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter, parents=[tools.argparser])


def setup_logging(level, logfile):
    format_str = '%(asctime)s %(levelname)s %(module)s::%(funcName)s (%(lineno)d) - %(message)s'
    formatter = logging.Formatter(format_str)
    logging.basicConfig( format=format_str, level=level, filename=logfile, filemode='w')
    root = logging.getLogger()
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    ch.setLevel(level)
    root.addHandler(ch)


def compare_files(file1, file2):
    import filecmp
    return filecmp.cmp(file1, file2)

json_path = os.path.join(os.sep, "Users", "daniel", "Documents", "Aktier", "JSON")
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



def main():
    general_args = parser.add_argument_group("General")
    general_args.add_argument("-v", "--verbose", action="store_true", help="Increase logging")
    general_args.add_argument("-l", "--logfile", dest="logfile", default="/tmp/stocks.log", help="Log output file")
    general_args.add_argument("--read", dest="read_transactions", action="store_true")
    general_args.add_argument("--no-read", dest="read_transactions", action="store_false")
    parser.set_defaults(read_transactions=True)
    general_args.add_argument("--write", dest="write_sheet", action="store_true")
    general_args.add_argument("--no-write", dest="write_sheet", action="store_false")
    parser.set_defaults(write_sheet=True)
    read_args = parser.add_argument_group("Read transactions from Avanza CSV export")
    write_args = parser.add_argument_group("Write transactions to Google Sheet")
    write_args.add_argument("--sheet_id", default="1B3ih0RL4zQ_4xV5yO28GDWQSjZRr8TVBYtVm4HGKPA0", help="Google Sheet Id")
    database_args = parser.add_argument_group("Database")
    database_args.add_argument("--database_path", default=os.path.join('data', 'stocks.db'), help="Path to sqlite db")
    database_args.add_argument("--data_structures", default=os.path.join('data', 'structures.sql'), help="Database structures")
    database_args.add_argument("--initial_data", default=os.path.join('data', 'initial_data.sql'), help="Initial data")
    database_args.add_argument("--setup_database", action="store_true")

    args = parser.parse_args()
    if args.database_path is None:
        parser.error("A database path must be provided")

    level = logging.INFO
    if args.verbose:
        level = logging.DEBUG
    setup_logging(level=level, logfile=args.logfile)

    db = Database(args.database_path, )
    if args.setup_database:
        db.setup(args.data_structures, args.initial_data)

    if args.read_transactions:
        new_transactions = read_transaction_rows_from_file(os.path.join(root_path, path_to_cvs_files))
        db.save_transactions(new_transactions)
        db.export_to_json(json_path)

    if args.write_sheet:
        sheet_id = args.sheet_id
        args = None
        sheet = GoogleSheet(sheet_id)
        dividends = db.get_transactions(transaction_type=["Dividend"])
        sheet.write_transactions("Utdelningar", dividends)

        transactions = db.get_transactions(transaction_type=["Deposit", "Withdrawal"])
        sheet.write_transactions("Transaktioner", transactions)

        today = datetime.now()
        start_date = datetime(today.year, 1, 1).strftime("%Y-%m-%d")
        end_date = datetime(today.year, today.month, today.day).strftime("%Y-%m-%d")
        stocks = db.get_all_stocks(in_portfolio=True, start_date=start_date, end_date=end_date)
        start_date = None
        end_date = None
        sheet.write_stock_summary("Portfolio", stocks, start_date, end_date)

        # for year in range(2016,2017):
        #      end_date = datetime(year, 12, 31).strftime("%Y-%m-%d")
        #      start_date = datetime(year, 12, 24).strftime("%Y-%m-%d")
        #      stocks = db.get_all_stocks(start_date=None, end_date=end_date, in_portfolio=True)
        #      sheet.write_stock_summary("%s" % year, stocks, start_date, end_date)

        #stocks = db.get_all_stocks(in_portfolio=False)
        #sheet.write_stock_summary("Old Portfolio", stocks)

if __name__ == "__main__":
    main()
    sys.exit(0)