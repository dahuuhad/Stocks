# -*- coding: utf-8 -*-

__author__ = 'daniel'
from datetime import datetime
import logging
from Transaction import Buy, Sell, Dividend, Transfer, Split, Deposit, Withdrawal, Tax


class Parser(object):
    def parse_row(self, date, account, transaction_type, description, units, price, amount, fee, currency, isin=None):
        logging.debug(account)
        if date == "Datum" or account == "Konto" or "Paulina" in account:
            logging.debug(account)
            return None
        transaction_type = transaction_type.decode('utf-8')
        description = description.decode('utf-8')
        logging.debug((date, account, transaction_type, description, units, price, amount, fee, currency))
        units = self.num(units)
        price = self.num(price)
        amount = self.num(amount)
        fee = self.num(fee)

        date_object = datetime.strptime(date, "%Y-%m-%d")
        logging.debug("%s == %s => %s" % (transaction_type, u"Utdelning", (transaction_type == u"Utdelning")))
        if self._ignore_transaction(account, transaction_type):
            logging.debug("Ignoring transaction %s" % ([date, account, transaction_type, description, units, price, amount, fee, currency]))
            return None
        if transaction_type == u"Utdelning":
            return Dividend(description, date, price, units)
        elif transaction_type == u"Köp" or transaction_type.startswith("Teckningslikvid") \
                or transaction_type.startswith("OMVANDLING") or transaction_type.startswith("BANCO SANT VP UTD") \
                or transaction_type.startswith("VP-UTD") or transaction_type.startswith("VPU AV MTG B"):
            #print date, transaction_type, description, units
            return Buy(description, date, price, units, amount)
        elif transaction_type == u"Sälj" or transaction_type == u"Köp, rättelse":
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
        elif transaction_type == u"Utländsk källskatt 15%":
            return None
            return Tax(date, amount)
        logging.error("Unknown transaction %s" % (
        [date, account, transaction_type, description, units, price, amount, fee, currency]))
        return None

    def _ignore_transaction(self, account, transaction_type):
        logging.debug("Transaction type: %s" % transaction_type)
        return "Paulina ISK" == account or "1455005" in transaction_type or "Roger" in transaction_type;

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
            logging.debug("Error when converting to int, trying float instead: %s" % s)
            return float(s)


    def _convert_units_by_transaction_type(self, transaction_type, units):
        if transaction_type.lower().startswith(u'övf till'):
            return -units
        return units

class AvanzaTransactionParser(Parser):
    pass

