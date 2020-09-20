# -*- coding: iso-8859-15 -*-

import os
from datetime import datetime
from string import ascii_uppercase

import httplib2
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse

    FLAGS = tools.argparser.parse_args(args=[])

except ImportError:
    FLAGS = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def _float_to_str(my_float):
    float_str = str(my_float).replace(".", ",")
    return float_str


def create_empty_rows(start_row, number_of_empty_rows):
    empty_rows = []
    for _ in range(start_row, start_row + number_of_empty_rows):
        empty_row = []
        for _ in ascii_uppercase:
            empty_row.append('')
        empty_rows.append(empty_row)
    return empty_rows


def insert_summary_row(start_row, end_row, summary_row_index):
    summary_row = []
    summary_columns = 'BCHILMPQR'
    for letter in ascii_uppercase:
        if letter == 'A':
            summary_row.append('Totalt')
        elif letter == 'D':
            summary_row.append('=(B{row}-H{row})/H{row}'.format(row=summary_row_index))
        elif letter in summary_columns:
            summary_row.append('=SUM({col}{}:{col}{})'.format(start_row, end_row, col=letter))
        else:
            summary_row.append('')
    return summary_row


def write_summary(sheet_name, transactions):
    start_row = 2
    start_col = 'A'
    range_name = '{sheet}!{col}{row}'.format(sheet=sheet_name, col=start_col, row=start_row)
    values = []
    for _ in reversed(transactions):
        transaction_list = ["=now()"]
        values.append(transaction_list)
    body = {
        'values': values
        }


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = tools.argparser.parse_args(args=[])
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def db_dividend_to_sheet(transaction, row):
    dividend_list = [str(transaction.date),
                     str(type(transaction).__name__),
                     str(transaction.stock),
                     _float_to_str(transaction.units),
                     _float_to_str(transaction.price),
                     "=D{row}*E{row}".format(row=row),
                     "=YEAR(A{row})".format(row=row),
                     "=MONTH(A{row})".format(row=row),
                     '=text(N(H{row})&"-1";"MMMM")'.format(row=row)]

    return dividend_list


def stock_to_history_row(stock, row, summary_row, start_date=None, end_date=None):
    stock_list = ['=HYPERLINK("{}"; "{}")'.format(stock.avanza_url, stock.name),
                  '={}*F{}'.format(stock.avanza_price, row),
                  '=IF({}=0;0;{}/{})'.format(_float_to_str(stock.sold_units),
                                             _float_to_str(stock.sold_sum),
                                             _float_to_str(stock.sold_units)),
                  '=IF({}=0;0;{}/{})'.format(_float_to_str(stock.sum_of_units),
                                             _float_to_str(stock.purchasing_sum),
                                             _float_to_str(stock.sum_of_units)),
                  '{}'.format(_float_to_str(stock.purchasing_sum))]
    #        stock_list.append('=%s*J%s' % (self._float_to_str(stock.get_price(start_date,
    #        end_date)), row)) ## E
    # J = Currency
    if stock.currency == "SEK":
        stock_list.append(1)
    else:
        stock_list.append('=GoogleFinance("CURRENCY:{}SEK")'.format(str(stock.currency)))

    stock_list.append('{}'.format(_float_to_str(stock.get_total_dividends())))
    stock_list.append('{}'.format(_float_to_str(stock.realized_gain)))
    stock_list.append('=G{0}+H{0}'.format(row))
    stock_list.append('=IF(I{0}=0;0;IF(E{0}=0;1,0;I{0}/E{0}))'.format(row))

    return stock_list


class GoogleSheet:

    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        discovery_url = ('https://sheets.googleapis.com/$discovery/rest?'
                         'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                                       discoveryServiceUrl=discovery_url)
        self.value_input_option = 'USER_ENTERED'

    def write_transactions(self, sheet_name, transactions):
        start_row = 2
        start_col = 'A'
        range_name = '{}!{}{}'.format(sheet_name, start_col, start_row)
        values = []
        row = start_row
        for transaction in reversed(transactions):
            if sheet_name == "Utdelningar":
                values.append(db_dividend_to_sheet(transaction, row))
            elif sheet_name == "Transaktioner":
                values.append(self.db_transaction_to_sheet(transaction, row))
            elif sheet_name == "Ränta":
                values.append(self.db_transaction_to_sheet(transaction, row))
            elif sheet_name == "Skatt":
                values.append(self.db_transaction_to_sheet(transaction, row))
            elif sheet_name == "Avgifter":
                values.append(self.db_transaction_to_sheet(transaction, row))
            row += 1
        body = {
            'values': values
            }
        result = self.service.spreadsheets(). \
            values().update(spreadsheetId=self.sheet_id,
                            range=range_name,
                            valueInputOption=self.value_input_option,
                            body=body).execute()

    def write_stock_summary(self, sheet_name, stocks, start_date=None, end_date=None):
        start_row = 2
        start_col = 'A'
        range_name = '{}!{}{}'.format(sheet_name, start_col, start_row)

        values = []

        row_id = start_row

        # stocks = [stock for stock in stocks if stock.total_units > 0]
        number_of_stocks = len(stocks)
        summary_row_index = 1 + number_of_stocks + 2 + 1

        for stock in stocks:
            row = self.stock_to_row(stock, row_id, summary_row_index, start_date, end_date)
            if not row:
                continue
            values.append(row)
            row_id += 1
        empty_rows = create_empty_rows(row_id, 2)
        values = values + empty_rows
        values.append(insert_summary_row(start_row, row_id - 1, summary_row_index))
        body = {
            'values': values
            }
        result = self.service.spreadsheets(). \
            values().update(spreadsheetId=self.sheet_id,
                            range=range_name,
                            valueInputOption=self.value_input_option,
                            body=body).execute()

    def write_stock_history(self, sheet_name, stocks, start_date=None, end_date=None):
        start_row = 2
        start_col = 'A'
        range_name = '{}!{}{}'.format(sheet_name, start_col, start_row)

        values = []

        row_id = start_row

        # stocks = [stock for stock in stocks if stock.total_units > 0]
        number_of_stocks = len(stocks)
        summary_row_index = 1 + number_of_stocks + 2 + 1

        for stock in stocks:
            row = stock_to_history_row(stock, row_id, summary_row_index, start_date, end_date)
            if not row:
                continue
            values.append(row)
            row_id += 1
        empty_rows = create_empty_rows(row_id, 2)
        values = values + empty_rows
        values.append(insert_summary_row(start_row, row_id - 1, summary_row_index))
        body = {
            'values': values
            }
        result = self.service.spreadsheets(). \
            values().update(spreadsheetId=self.sheet_id,
                            range=range_name,
                            valueInputOption=self.value_input_option,
                            body=body).execute()

    def stock_to_row(self, stock, row, summary_row, start_date=None, end_date=None):
        stock_list = ['=HYPERLINK("{}"; "{}")'.format(stock.avanza_url, stock.name),
                      '=E{0}*F{0}'.format(row),
                      '=B{0}-H{0}'.format(row),
                      '=IF(H{0}=0;B{0}/100;C{0}/H{0})'.format(row),
                      '={}*J{}'.format(stock.avanza_price, row),
                      '{}'.format(_float_to_str(stock.total_units)),
                      '{}'.format(_float_to_str(stock.get_total_price())),
                      '=G{0}*F{0}'.format(row),
                      '=B{}/B{}'.format(row, summary_row)]
        #        stock_list.append('=%s*J%s' % (self._float_to_str(stock.get_price(start_date,
        #        end_date)), row)) ## E
        # J = Currency
        if stock.currency == "SEK":
            stock_list.append(1)
        else:
            stock_list.append('=GoogleFinance("CURRENCY:{}SEK")'.format(str(stock.currency)))
        # K = Utdelning/Aktie
        stock_list.append(
            '=J{row}*{}*T{row}'.format(_float_to_str(stock.get_dividend_forecast()), row=row))
        # L = Arets utdelning
        if start_date and end_date:
            stock_list.append(
                '={}'.format(_float_to_str(stock.get_total_dividends(start_date, end_date))))
        else:
            stock_list.append('={}'.format(_float_to_str(
                stock.get_total_dividends(datetime(datetime.today().year, 1, 1).date(),
                                          datetime(datetime.today().year, 12, 31).date()))))

        # M = Utdelningsprognos
        stock_list.append('=F{0}*K{0}'.format(row))
        stock_list.append('=IF(G{0}=0;0; K{0}/G{0})'.format(row))
        stock_list.append('=K{0}/E{0}'.format(row))
        stock_list.append('{}'.format(_float_to_str(stock.get_total_dividends())))
        stock_list.append('{}'.format(_float_to_str(stock.realized_gain)))
        stock_list.append('=P{0}+Q{0}'.format(row))
        stock_list.append('=IF(H{0}=0;B{0}/100;R{0}/H{0})'.format(row))
        stock_list.append('{}'.format(_float_to_str(stock.dividend_per_year)))

        return stock_list

    def db_transaction_to_sheet(self, transaction, row):
        transaction_list = [str(transaction.date), str(type(transaction).__name__),
                            _float_to_str(transaction.amount), "=YEAR(A%s)" % row,
                            "=MONTH(A%s)" % row,
                            '=text(N(E%s)&"-1";"MMMM")' % row]

        return transaction_list

    def read_stocks(self):
        range_name = 'Innehav!A2:E15'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id, range=range_name).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print('Name, Major:')
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                print('{}, {}'.format(row[0], row[4]))

        values = [
            [
                "AAPL", "=3+3", "4", "=GoogleFinance(\"NASDAQ:AAPL\")"
                ],
            # Additional rows ...
            ]
        body = {
            'values': values
            }
        range_name = 'Innehav!A20:E'
        value_input_option = 'USER_ENTERED'
