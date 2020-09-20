# -*- coding: iso-8859-15 -*-

__author__ = 'daniel'
import logging

from Transaction import Buy, Deposit, Dividend, Earning, Fee, Sell, Split, Tax, Transfer, Withdrawal


def _convert_units_by_transaction_type(transaction_type, units):
    if transaction_type.lower().startswith(u'�vf till'):
        return -units
    return units


def _transaction_is_transfer(transaction_type):
    # print transaction_type, transaction_type.startswith(u'�verf�ring'),
    # transaction_type.startswith(u'�vf')
    return transaction_type.startswith(u'�verf�ring') or transaction_type.lower().startswith(u'�vf')


def _ignore_transaction(account, transaction_type):
    logging.debug("Transaction type: %s", transaction_type)
    return account == "Paulina ISK" or "1455005" in transaction_type or "Roger" in transaction_type


def _transaction_is_buy(transaction_type):
    if transaction_type == u"K�p":
        return True
    startswith_list = ["Teckningslikvid", "OMVANDLING", "BANCO SANT VP UTD",
                       "VP-UTD", "VPU AV MTG B", "Avknoppning", "Inl"]
    for transaction_str in startswith_list:
        if transaction_type.startswith(transaction_str):
            return True
    return False


class Parser:

    def parse_row(self, date, account, transaction_type, description, units, price,
                  amount, fee, currency, isin=None):
        logging.debug(account)
        if date == "Datum" or account == "Konto" or "Paulina" in account:
            logging.debug(account)
            return None
        logging.debug((date, account, transaction_type, description, units,
                       price, amount, fee, currency))
        units = self.num(units)
        price = self.num(price)
        amount = self.num(amount)
        fee = self.num(fee)

        logging.debug("%s == %s => %s", transaction_type, u"Utdelning",
                      (transaction_type == u"Utdelning"))
        if _ignore_transaction(account, transaction_type):
            logging.debug("Ignoring transaction %s", [date, account, transaction_type, description,
                                                      units, price, amount, fee, currency])
            return None
        if transaction_type == u"Utdelning":
            return Dividend(description, date, price, units)
        elif _transaction_is_buy(transaction_type):
            return Buy(description, date, price, units, amount)
        elif transaction_type in (u"S�lj", u"K�p, r�ttelse"):
            return Sell(description, date, price, units, amount)
        elif transaction_type in (u"Split", u"Omv�nd split"):
            return Split(description, date, units)
        elif _transaction_is_transfer(transaction_type):
            units = _convert_units_by_transaction_type(transaction_type, units)
            return Transfer(description, date, units)
        elif transaction_type == u"Ins�ttning":
            return Deposit(date, amount)
        elif transaction_type == u"Uttag":
            return Withdrawal(date, amount)
        elif transaction_type == u"Prelskatt utdelningar" or \
                (transaction_type == u"�vrigt" and "k�llskatt" in description) or \
                transaction_type.startswith(u"Utl�ndsk k�llskatt") or \
                transaction_type == u"Prelimin�rskatt" or \
                (transaction_type == u"�vrigt" and description == u"Avkastningsskatt"):
            return Tax(date, amount)
        elif transaction_type == u"�vrigt" and description == u"Riskpremie":
            return Fee(date, amount)
        elif transaction_type == u"R�ntor" or \
                (
                        transaction_type == u"�vrigt" and description == u"�verf�ring r�nta "
                                                                         u"kapitalmedelskonto"):
            return Earning(date, amount)
        logging.error("Unknown transaction %s", [date, account, transaction_type, description,
                                                 units, price, amount, fee, currency])
        return None

    @staticmethod
    def num(my_str):
        try:
            my_str = my_str.replace(',', '.')
            if len(my_str) == 1:
                my_str = my_str.replace('-', '0')
            return int(my_str)
        except ValueError:
            logging.debug("Error when converting to int, trying float instead: %s", my_str)
            return float(my_str)


class AvanzaTransactionParser(Parser):
    pass
