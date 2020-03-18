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

    flags = tools.argparser.parse_args(args=[])

    # flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def _float_to_str(f):
    float_str = str(f).replace(".", ",")
    if f < 0.0:
        float_str = float_str
    return float_str


def create_empty_rows(start_row, number_of_empty_rows):
    empty_rows = []
    for i in range(start_row, start_row + number_of_empty_rows):
        empty_row = []
        for c in ascii_uppercase:
            empty_row.append('')
        empty_rows.append(empty_row)
    return empty_rows


def insert_summary_row(start_row, end_row, summary_row_index):
    summary_row = []
    summary_columns = 'BCHILMPQR'
    for c in ascii_uppercase:
        if c == 'A':
            summary_row.append('Totalt')
        elif c == 'D':
            summary_row.append('=(B%s-H%s)/H%s' % (summary_row_index, summary_row_index, summary_row_index))
        elif c in summary_columns:
            summary_row.append('=SUM(%s%s:%s%s)' % (c, start_row, c, end_row))
        else:
            summary_row.append('')
    return summary_row


def write_summary(sheet_name, transactions):
    start_row = 2
    start_col = 'A'
    range_name = '%s!%s%s' % (sheet_name, start_col, start_row)
    values = []
    for transaction in reversed(transactions):
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


class GoogleSheet:

    def __init__(self, sheet_id):
        self.sheetId = sheet_id
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
        range_name = '%s!%s%s' % (sheet_name, start_col, start_row)
        values = []
        row = start_row
        for transaction in reversed(transactions):
            if sheet_name == "Utdelningar":
                values.append(self.db_dividend_to_sheet(transaction, row))
            elif sheet_name == "Transaktioner":
                values.append(self.db_transaction_to_sheet(transaction, row))
            row += 1
        body = {
            'values': values
            }
        result = self.service.spreadsheets().values().update(spreadsheetId=self.sheetId, range=range_name,
                                                             valueInputOption=self.value_input_option,
                                                             body=body).execute()

    def write_stock_summary(self, sheet_name, stocks, start_date=None, end_date=None):
        start_row = 2
        start_col = 'A'
        range_name = '%s!%s%s' % (sheet_name, start_col, start_row)

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
        result = self.service.spreadsheets().values().update(spreadsheetId=self.sheetId, range=range_name,
                                                             valueInputOption=self.value_input_option,
                                                             body=body).execute()

    def write_stock_history(self, sheet_name, stocks, start_date=None, end_date=None):
        start_row = 2
        start_col = 'A'
        range_name = '%s!%s%s' % (sheet_name, start_col, start_row)

        values = []

        row_id = start_row

        # stocks = [stock for stock in stocks if stock.total_units > 0]
        number_of_stocks = len(stocks)
        summary_row_index = 1 + number_of_stocks + 2 + 1

        for stock in stocks:
            row = self.stock_to_history_row(stock, row_id, summary_row_index, start_date, end_date)
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
        result = self.service.spreadsheets().values().update(spreadsheetId=self.sheetId, range=range_name,
                                                             valueInputOption=self.value_input_option,
                                                             body=body).execute()

    def stock_to_history_row(self, stock, row, summary_row, start_date=None, end_date=None):
        stock_list = ['=HYPERLINK("%s"; "%s")' % (stock.avanza_url, stock.name),
                      '=%s*F%s' % (stock.avanza_price, row),
                      '=IF(%s=0;0;%s/%s)' % (
                      _float_to_str(stock.sold_units), _float_to_str(stock.sold_sum), _float_to_str(stock.sold_units)),
                      '=IF(%s=0;0;%s/%s)' % (_float_to_str(stock.sum_of_units), _float_to_str(stock.purchasing_sum),
                                             _float_to_str(stock.sum_of_units)),
                      '%s' % _float_to_str(stock.purchasing_sum)]
        #        stock_list.append('=%s*J%s' % (self._float_to_str(stock.get_price(start_date, end_date)), row)) ## E
        # J = Currency
        if stock.currency == "SEK":
            stock_list.append(1)
        else:
            stock_list.append('=GoogleFinance("CURRENCY:%sSEK")' % str(stock.currency))

        stock_list.append('%s' % _float_to_str(stock.get_total_dividends()))
        stock_list.append('%s' % _float_to_str(stock.realized_gain))
        stock_list.append('=F%s+G%s' % (row, row))
        stock_list.append('=IF(H%s=0;0;IF(D%s=0;1,0;H%s/D%s))' % (row, row, row, row))

        return stock_list

    def stock_to_row(self, stock, row, summary_row, start_date=None, end_date=None):
        stock_list = ['=HYPERLINK("%s"; "%s")' % (stock.avanza_url, stock.name), '=E%s*F%s' % (row, row),
                      '=B%s-H%s' % (row, row), '=IF(H%s=0;B%s/100;C%s/H%s)' % (row, row, row, row),
                      '=%s*J%s' % (stock.avanza_price, row), '%s' % _float_to_str(stock.total_units),
                      '%s' % _float_to_str(stock.get_total_price()), '=G%s*F%s' % (row, row),
                      '=B%s/B%s' % (row, summary_row)]
        #        stock_list.append('=%s*J%s' % (self._float_to_str(stock.get_price(start_date, end_date)), row)) ## E
        # J = Currency
        if stock.currency == "SEK":
            stock_list.append(1)
        else:
            stock_list.append('=GoogleFinance("CURRENCY:%sSEK")' % str(stock.currency))
        # K = Utdelning/Aktie
        stock_list.append('=J%s*%s*T%s' % (row, _float_to_str(stock.get_dividend_forecast()), row))
        # L = Arets utdelning
        if start_date and end_date:
            stock_list.append('=%s' % (_float_to_str(stock.get_total_dividends(start_date, end_date))))
        else:
            stock_list.append('=%s' % (_float_to_str(
                stock.get_total_dividends(datetime(datetime.today().year, 1, 1).date(),
                                          datetime(datetime.today().year, 12, 31).date()))))

        # M = Utdelningsprognos
        stock_list.append('=F%s*K%s' % (row, row))
        stock_list.append('=IF(G14=0;0; K%s/G%s)' % (row, row))
        stock_list.append('=K%s/E%s' % (row, row))
        stock_list.append('%s' % _float_to_str(stock.get_total_dividends()))
        stock_list.append('%s' % _float_to_str(stock.realized_gain))
        stock_list.append('=P%s+Q%s' % (row, row))
        stock_list.append('=IF(H%s=0;B%s/100;R%s/H%s)' % (row, row, row, row))
        stock_list.append('%s' % _float_to_str(stock.dividend_per_year))

        return stock_list

    def db_dividend_to_sheet(self, transaction, row):
        dividend_list = [str(transaction.date), str(type(transaction).__name__), str(transaction.stock),
                         _float_to_str(transaction.units), _float_to_str(transaction.price),
                         "=D%s*E%s" % (row, row), "=YEAR(A%s)" % row, "=MONTH(A%s)" % row,
                         '=text(N(H%s)&"-1";"MMMM")' % row]

        return dividend_list

    def db_transaction_to_sheet(self, transaction, row):
        transaction_list = [str(transaction.date), str(type(transaction).__name__),
                            _float_to_str(transaction.amount), "=YEAR(A%s)" % row, "=MONTH(A%s)" % row,
                            '=text(N(E%s)&"-1";"MMMM")' % row]

        return transaction_list

    def read_stocks(self):
        range_name = 'Innehav!A2:E15'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetId, range=range_name).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print('Name, Major:')
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                print('%s, %s' % (row[0], row[4]))

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
