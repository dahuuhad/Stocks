__author__ = 'daniel'

import csv
import os
import logging
from operator import itemgetter
from data.DataSource import CvsDataSource
from parser.Parser import AvanzaTransactionParser
from reports.Report import PlainReport
from tabulate import tabulate
from Stock import Stock


def setup_logging():
    logging.basicConfig( format='%(asctime)s %(levelname)s %(module)s::%(funcName)s (%(lineno)d) - %(message)s', level=logging.DEBUG)



def compare_files(file1, file2):
    import filecmp
    return filecmp.cmp(file1, file2)


root_path = os.path.join(os.sep, "Users", "daniel", "Documents", "Aktier")
stock_file = "Stocks.txt"
path_to_cvs_files = "transactions"
report_path = "reports"


def main():
    setup_logging()
    logging.info("Reading cvs data source")
    data_source = CvsDataSource(root_path, path_to_cvs_files, stock_file)
    stocks = data_source.get_stocks()

    dividends = data_source.get_transactions("dividend")
    transactions = data_source.get_transactions("all")
    logging.info("Found %s transactions" % len(transactions))
    plain_report = PlainReport(os.path.join(root_path, report_path))
    # plain_report.generate_stock_summary(stocks)
    plain_report.generate_transaction_history("dividends_history.txt", dividends)
    plain_report.generate_dividend_summary("divident_summary.txt", dividends)

    plain_report.generate_stock_depot("stock_depot.txt", transactions)

    #assert compare_files(os.path.join(root_path, report_path, "stock_depot.txt"), os.path.join(root_path, report_path, "stock_facit.txt"))
    #cvs_report = CSVReport(os.path.join(root_path, report_path))
    #plain_report.generate_transaction_history("dividends_history.csv", dividends)



def read_stocks_from_file(stock_file):
    stocks = []
    with open(stock_file, 'r') as f:
        reader = csv.reader(f, dialect='excel', delimiter=';')
        for row in reader:
            if row[-1] == "Aktie":
                stocks.append(Stock(*row))
    return stocks

def find_stock_for_transaction(stocks, transaction):
    for stock in stocks:
        if stock.key == transaction.stock:
            return stock
    return None


def read_transaction_rows_from_file(transaction_path, stocks):
    transactions = []
    transaction_parser = AvanzaTransactionParser()
    if os.path.isdir(transaction_path):
        for file_name in sorted(os.listdir(transaction_path)):
            if os.path.splitext(file_name)[1] == ".csv":
                logging.info("Parsing %s" % file_name)
                with open(os.path.join(transaction_path, file_name), 'r') as f:
                    reader = csv.reader(f, dialect='excel', delimiter=';')
                    for row in reader:
                        transaction = transaction_parser.parse_row(*row)
                        if transaction:
                            stock = find_stock_for_transaction(stocks, transaction)
                            if stock:
                                stock.add_transaction(transaction)


def print_stock_summary(stocks):
    logging.info("Printing stock summary")
    summary_header = ["Stock", "Units", "Price", "Value"]
    summary_data = []
    for stock in stocks:
        summary_data  = summary_data + stock.get_summary()
    print tabulate(sorted(summary_data, key=itemgetter(0)), summary_header)

def main2():
    stocks = read_stocks_from_file(os.path.join(root_path, stock_file))
    logging.debug(stocks)
    read_transaction_rows_from_file(os.path.join(root_path, path_to_cvs_files), stocks)
    logging.info("Number of stocks: %s" % len(stocks))
    print_stock_summary(stocks)
    return 0

if __name__ == "__main__":
    #main()
    setup_logging()
    main2()
    exit(0)