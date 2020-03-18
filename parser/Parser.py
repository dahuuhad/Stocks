# -*- coding: utf-8 -*-

__author__ = 'daniel'
import logging

from Transaction import Buy, Sell, Dividend, Transfer, Split, Deposit, Withdrawal, Tax


def _convert_units_by_transaction_type(transaction_type, units):
    if transaction_type.lower().startswith(u'övf till'):
        return -units
    return units


def _transaction_is_transfer(transaction_type):
    # print transaction_type, transaction_type.startswith(u'Överföring'), transaction_type.startswith(u'Övf')
    return transaction_type.startswith(u'Överföring') or transaction_type.lower().startswith(u'övf')


def _ignore_transaction(account, transaction_type):
    logging.debug("Transaction type: %s" % transaction_type)
    return "Paulina ISK" == account or "1455005" in transaction_type or "Roger" in transaction_type


class Parser(object):
    def parse_row(self, date, account, transaction_type, description, units, price, amount, fee, currency, isin=None):
        logging.debug(account)
        if date == "Datum" or account == "Konto" or "Paulina" in account:
            logging.debug(account)
            return None
        logging.debug((date, account, transaction_type, description, units, price, amount, fee, currency))
        units = self.num(units)
        price = self.num(price)
        amount = self.num(amount)
        fee = self.num(fee)

        logging.debug("%s == %s => %s" % (transaction_type, u"Utdelning", (transaction_type == u"Utdelning")))
        if _ignore_transaction(account, transaction_type):
            logging.debug("Ignoring transaction %s" % ([date, account, transaction_type, description,
                                                        units, price, amount, fee, currency]))
            return None
        if transaction_type == u"Utdelning":
            return Dividend(description, date, price, units)
        elif transaction_type == u"Köp" or transaction_type.startswith("Teckningslikvid") \
                or transaction_type.startswith("OMVANDLING") or transaction_type.startswith("BANCO SANT VP UTD") \
                or transaction_type.startswith("VP-UTD") or transaction_type.startswith("VPU AV MTG B") \
                or transaction_type.startswith("Avknoppning") or transaction_type.startswith("Inl"):
            return Buy(description, date, price, units, amount)
        elif transaction_type == u"Sälj" or transaction_type == u"Köp, rättelse":
            return Sell(description, date, price, units, amount)
        elif transaction_type == u"Split" or transaction_type == u"Omvänd split":
            return Split(description, date, units)
        elif _transaction_is_transfer(transaction_type):
            units = _convert_units_by_transaction_type(transaction_type, units)
            return Transfer(description, date, units)
        elif transaction_type == u"Insättning":
            return Deposit(date, amount)
        elif transaction_type == u"Uttag":
            return Withdrawal(date, amount)
        elif transaction_type == u"Utländsk källskatt 15%":
            return Tax(date, amount)
        logging.error("Unknown transaction %s" % ([date, account, transaction_type, description,
                                                   units, price, amount, fee, currency]))
        return None

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


class AvanzaTransactionParser(Parser):
    pass
