# -*- coding: utf-8 -*-

__author__ = 'daniel'
from datetime import datetime
import logging
from Transaction import Buy, Sell, Dividend, Transfer, Split, Deposit, Withdrawal


class Parser(object):
    def parse_row(self, date, account, transaction_type, description, units, price, amount, fee, currency, isin=None):
        if date == "Datum" or account == "Konto":
            return None
        logging.debug((date, account, units))
        units = self.num(units)
        price = self.num(price)
        amount = self.num(amount)
        fee = self.num(fee)

        date_object = datetime.strptime(date, "%Y-%m-%d")
        transaction_type = transaction_type.decode("latin1")
        logging.debug("%s" % ([date, transaction_type, description.decode("latin1"), units, price, amount, currency]))

        if self._ignore_transaction(transaction_type):
            logging.debug("Ignoring transaction %s %s" % (date, transaction_type))
            return None

        if transaction_type == u"Utdelning":
            return Dividend(description, date, price, units)
        elif transaction_type == u"Köp" or transaction_type.startswith("Teckningslikvid") \
                or transaction_type.startswith("OMVANDLING") or transaction_type.startswith("BANCO SANT VP UTD") \
                or transaction_type.startswith("VP-UTD") or transaction_type.startswith("VPU AV MTG B"):
            #print date, transaction_type, description, units
            return Buy(description, date, price, units, amount)
        elif transaction_type == u"Sälj":
            #print date, transaction_type, description, units
            return Sell(description, date, price, units, amount)
        elif transaction_type == u"Split" or transaction_type == u"Omvänd split":
            #print date, transaction_type, description, units
            return Split(description, date, units)
        elif self._transaction_is_transfer(transaction_type):
            units = self._convert_units_by_transaction_type(transaction_type, units)
            return Transfer(description, date, units)
        elif transaction_type == u"Insättning":
            return Deposit(date, amount)
        elif transaction_type == u"Uttag":
            return Withdrawal(date, amount)

        return None

    def _ignore_transaction(self, transaction_type):
        logging.debug("Transaction type: %s" % transaction_type)
        return "1455005" in transaction_type or "Roger" in transaction_type;

    def _transaction_is_transfer(self, transaction_type):
        # print transaction_type, transaction_type.startswith(u'Överföring'), transaction_type.startswith(u'Övf')
        return transaction_type.startswith(u'Överföring') or transaction_type.lower().startswith(u'övf')


    @staticmethod
    def num(s):
        try:
            s = s.replace(',', '.')
            if len(s) == 1:
                s = s.replace('-', '0')
            return int(s)
        except ValueError:
            logging.debug("Value error: %s" % s)
            return float(s)


    def _convert_units_by_transaction_type(self, transaction_type, units):
        if transaction_type.lower().startswith(u'övf till'):
            return -units
        return units

class AvanzaTransactionParser(Parser):
    pass

