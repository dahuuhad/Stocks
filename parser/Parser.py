# -*- coding: utf-8 -*-

__author__ = 'daniel'
from datetime import datetime

from Transaction import Buy, Sell, Dividend, Transfer, Split


class Parser(object):
    def __init__(self):
        self._stocks_to_ignore = ['Catella B', 'DSP']


class AvanzaTransactionParser(Parser):
    def __init__(self):
        super(AvanzaTransactionParser, self).__init__()
        self._stock_translator = dict()
        self._init_stock_translator()

    def _init_stock_translator(self):
        self._stock_translator['AAPL'] = "Apple Inc"
        self._stock_translator['KOP'] = "Kopparbergs B"
        self._stock_translator['VARD'] = "Vardia Insurance Group"
        self._stock_translator['FING'] = "FING B"
        self._stock_translator['NOK'] = "NOKI SDB, Nokia Oyj"
        self._stock_translator['VOLV'] = "VOLV IL B, Volvo B, Volvo DR B"
        self._stock_translator['ATL'] = "Atlant Stability"
        self._stock_translator['SAN'] = "Banco Santander SA"
        self._stock_translator['BON'] = "Bonheur"
        self._stock_translator['CLAS'] = "Clas Ohlson B"
        self._stock_translator['KO'] = "Coca-Cola Co"
        self._stock_translator['DE'] = "Deere & Co"
        self._stock_translator['ERIC'] = "Ericsson B"
        self._stock_translator['SHB'] = "Handelsbanken, SHB, SHB B OLD"
        self._stock_translator['HM'] = "Hennes & Mauritz B"
        self._stock_translator['INDU'] = u"Industrivärden C"
        self._stock_translator['INVE'] = "Investor B"
        self._stock_translator['MCD'] = "McDonald's Corp"
        self._stock_translator['PROT'] = "Protector Forsikring"
        self._stock_translator['CAST'] = "Castellum"
        self._stock_translator['CIT'] = "Citigroup"
        self._stock_translator['SMP'] = "Sampo A"
        self._stock_translator['TEL'] = "Telia Company"
        self._stock_translator['NOVO'] = "Novo Nordisk B"

        self._stock_translator['WAL'] = "Walmart"
        self._stock_translator['SWED'] = "Swedbank A"
        self._stock_translator['SBUX'] = "Starbucks Corp"
        self._stock_translator['RAT'] = "Ratos B"
        self._stock_translator['NCC'] = "Ncc B"
        self._stock_translator['SKAN'] = "Skanska B"
        self._stock_translator['AVAZ'] = "Avanza Zero"
        self._stock_translator['CAR'] = "Carnegie Rysslandsfond"

    def _get_stock_from_transaction(self, description):
        for key, stock in self._stock_translator.iteritems():
            if description in stock:
                return key
        return None

    def parse_row(self, date, account, transaction_type, description, units, price, cost, currency, isin=None):
        if date == "Datum" and account == "Konto":
            return None
        #description = self._get_stock_from_transaction(description.decode("latin1"))
        #if not description:
        #    return
        units = self.num(units)
        price = self.num(price)
        cost = self.num(cost)
        fee = cost - units*price
        date_object = datetime.strptime(date, "%Y-%m-%d")
        transaction_type = transaction_type.decode("latin1")
        #print date, transaction_type, description, units, price, cost, currency
        if transaction_type == u"Utdelning":
            return Dividend(description, date_object, price, units)
        elif transaction_type == u"Köp" or transaction_type.startswith("Nyteckning") \
                or transaction_type.startswith("OMVANDLING") or transaction_type.startswith("BANCO SANT VP UTD"):
            #print date, transaction_type, description, units
            return Buy(description, date_object, price, units, fee)
        elif transaction_type == u"Sälj":
            #print date, transaction_type, description, units
            return Sell(description, date_object, price, units, fee)
        elif transaction_type == u"Split" or transaction_type == u"Omvänd split":
            #print date, transaction_type, description, units
            return Split(description, date_object, units)
        elif self._transaction_is_transfer(transaction_type):
            units = self._convert_units_by_transaction_type(transaction_type, units)
            return Transfer(description, date_object, units)

        return None

    def _transaction_is_transfer(self, transaction_type):
        #print transaction_type, transaction_type.startswith(u'Överföring'), transaction_type.startswith(u'Övf')
        return transaction_type.startswith(u'Överföring') or transaction_type.lower().startswith(u'övf')

    @staticmethod
    def num(s):
        try:
            s = s.replace(',','.')
            s = s.replace('-','0')
            return int(s)
        except ValueError:
            return float(s)

    def _convert_units_by_transaction_type(self, transaction_type, units):
        if transaction_type.lower().startswith(u'övf till'):
            return -units
        return units