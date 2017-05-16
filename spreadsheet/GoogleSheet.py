#from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from datetime import datetime
from string import ascii_uppercase
import logging

try:
    import argparse
    flags=tools.argparser.parse_args(args=[])

    #flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


class GoogleSheet():

    def __init__(self, sheetId):
        self.sheetId = sheetId
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)
        self.value_input_option = 'USER_ENTERED'

    def get_credentials(self):
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
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run_flow(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def write_transactions(self, sheet_name, transactions):
        start_row = 2
        start_col = 'A'
        rangeName = '%s!%s%s' % (sheet_name, start_col, start_row)
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
        result = self.service.spreadsheets().values().update(spreadsheetId=self.sheetId, range=rangeName,
                                                             valueInputOption=self.value_input_option, body=body).execute()

    def insert_summary_row(self, start_row, end_row, summary_row_index):
        summary_row = []
        summary_columns = 'BCHILOPQ'
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

    def create_empty_rows(self, start_row, number_of_empty_rows):
        empty_rows = []
        for i in range(start_row, start_row+number_of_empty_rows):
            empty_row =[]
            for c in ascii_uppercase:
                empty_row.append('')
            empty_rows.append(empty_row)
        return empty_rows

    def write_stock_summary(self, sheet_name, stocks, start_date=None, end_date=None):
        start_row = 2
        start_col = 'A'
        rangeName = '%s!%s%s' % (sheet_name, start_col, start_row)

        values = []

        row_id = start_row

        #stocks = [stock for stock in stocks if stock.total_units > 0]
        number_of_stocks = len(stocks)
        summary_row_index = 1+number_of_stocks+2+1

        for stock in stocks:
            row = self.stock_to_row(stock, row_id, summary_row_index, start_date, end_date)
            if not row:
                continue
            values.append(row)
            row_id += 1
        empty_rows = self.create_empty_rows(row_id, 2)
        values = values + empty_rows
        values.append(self.insert_summary_row(start_row, row_id-1, summary_row_index))
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().update(spreadsheetId=self.sheetId, range=rangeName,
                                                             valueInputOption=self.value_input_option, body=body).execute()


    def stock_to_row(self, stock, row, summary_row, start_date=None, end_date=None):
        l = []
        l.append(str(stock.name.encode("utf8")))
        l.append('=E%s*F%s' % (row, row))
        l.append('=B%s-H%s' % (row, row))
        l.append('=C%s/H%s' % (row, row))
        l.append('=%s*J%s' % (self._float_to_str(stock.get_price(start_date, end_date)), row))
        l.append('%s' % self._float_to_str(stock.total_units))
        l.append('%s' % self._float_to_str(stock.get_total_price()))
        l.append('=G%s*F%s' % (row, row))
        l.append('=B%s/B%s' % (row, summary_row))
        if stock.currency == "SEK":
            l.append(1)
        else:
            l.append('=GoogleFinance("CURRENCY:%sSEK")' % str(stock.currency))
        l.append('=J%s*%s*%s' % (row, self._float_to_str(stock.get_dividend_forecast()), stock.dividend_per_year))
        l.append('=F%s*K%s' % (row, row))
        l.append('=K%s/G%s' % (row, row))
        l.append('=K%s/E%s' % (row, row))
        l.append('%s' % self._float_to_str(stock.get_total_dividends()))
        l.append('%s' % self._float_to_str(stock.realized_gain))
        l.append('=O%s+P%s' % (row, row))

        return l

    def db_dividend_to_sheet(self, transaction, row):
        l = []

        l.append(datetime.strptime(str(transaction.date), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"))
        l.append(str(type(transaction).__name__))
        l.append(str(transaction.stock.encode("utf8")))
        l.append(self._float_to_str(transaction.units))
        l.append(self._float_to_str(transaction.price))
        l.append("=D%s*E%s" % (row, row))
        l.append("=YEAR(A%s)" % row)
        l.append("=MONTH(A%s)" % row)
        l.append('=text(N(H%s)&"-1";"MMMM")' % row)

        return l

    def db_transaction_to_sheet(self, transaction, row):
        l = []

        l.append(datetime.strptime(str(transaction.date), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"))
        l.append(str(type(transaction).__name__))
        l.append(self._float_to_str(transaction.amount))
        l.append("=YEAR(A%s)" % row)
        l.append("=MONTH(A%s)" % row)
        l.append('=text(N(E%s)&"-1";"MMMM")' % row)

        return l

    def _float_to_str(self, f):

        float_str = str(f).replace(".", ",")
        if f < 0.0:
            float_str = "-"+float_str
        return float_str

    def read_stocks(self):
        rangeName = 'Innehav!A2:E15'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetId, range=rangeName).execute()
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
        rangeName = 'Innehav!A20:E'
        value_input_option = 'USER_ENTERED'
        result = self.service.spreadsheets().values().update(spreadsheetId=self.sheetId, range=rangeName,
                                                        valueInputOption=value_input_option, body=body).execute()


