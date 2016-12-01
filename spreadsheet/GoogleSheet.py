#from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from datetime import datetime
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
        for transaction in transactions:
            print transaction
            values.append(self.db_transaction_to_sheet(transaction, row))
            row += 1
        body = {
            'values': values
        }
        print values
        print body
        result = self.service.spreadsheets().values().update(spreadsheetId=self.sheetId, range=rangeName,
                                                             valueInputOption=self.value_input_option, body=body).execute()

    def write_stock_summary(self, sheet_name, stocks):
        start_row = 2
        start_col = 'A'
        rangeName = '%s!%s%s' % (sheet_name, start_col, start_row)

        values = []
        row = start_row
        for stock in stocks:
            values.append(self.stock_to_row(stock, row))
            row += 1

        body = {
            'values': values
        }
        print values
        print body
        result = self.service.spreadsheets().values().update(spreadsheetId=self.sheetId, range=rangeName,
                                                             valueInputOption=self.value_input_option, body=body).execute()

    def stock_to_row(self, stock, row):
        summary = stock.get_summary()
        if not summary:
            print stock.name
            return []
        print summary
        total = 100000
        l = []
        l.append(str(stock.name.encode("utf8")))
        l.append('=H%s*G%s' % (row, row))
        l.append('=B%s-J%s' % (row, row))
        l.append('=C%s/J%s' % (row, row))
        l.append('=GoogleFinance(L%s;"pe")' % row)
        l.append('=GoogleFinance(L%s;"eps")' % row)
        l.append('=GoogleFinance(L%s) * M2' % row)
        l.append('%s' % summary[0][1])
        l.append('100,00')
        l.append('=H%s*I%s' % (row, row))
        l.append('=B%s/%s' % (row, total))
        l.append(str(stock.google_quote))
        if stock.currency == "SEK":
            l.append(1)
        else:
            l.append('=GoogleFinance("CURRENCY:%sSEK")' % str(stock.currency))
        l.append('=GoogleFinance(L%s;"incomedividend")' % row)
        l.append('=N%s*H%s' % (row, row))
        l.append('=O%s/J%s' % (row, row))
        return l

    def db_transaction_to_sheet(self, transaction, row):
        l = []
        l.append(datetime.strptime(str(transaction.get('trans_date')), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"))
        l.append(str(transaction.get('trans_type')))
        l.append(str(transaction.get('name').encode("utf8")))
        l.append(self._float_to_str(transaction.get('units')))
        l.append(self._float_to_str(transaction.get('price')))
        l.append("=D%s*E%s" % (row, row))
        l.append("=YEAR(A%s)" % row)
        l.append("=MONTH(A%s)" % row)
        l.append('=text(N(H%s)&"-1";"MMMM")' % row)

        return l

    def _float_to_str(self, f):
        return str(f).replace(".", ",")

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
