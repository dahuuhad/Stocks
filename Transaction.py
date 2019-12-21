# -*- coding: utf-8 -*-
__author__ = 'daniel'

from datetime import datetime


def _string_to_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').date()

class Transaction(object):
    def __init__(self, type, stock, date):
        self.stock = stock
        self.date = _string_to_date(date)
        self.units = 0.0
        self.price = 0.0
        self.amount = 0.0
        self.str_type = type

    def __str__(self):
        return "Type=%s, Date=%s, Stock=%s" % (self.str_type, self.date, self.stock)

    @classmethod
    def to_table_header(cls):
        return ["Stock", "Date"]

    def to_table(self):
        return [self.stock, self.date]

    def to_csv(self):
        return ",".join(self.to_table())


class Transfer(Transaction):
    def __init__(self, stock, date, units):
        super(Transfer, self).__init__("Transfer", stock, date)
        self.units = units

    @classmethod
    def to_table_header(cls):
        table_header = super(Transfer, cls).to_table_header()
        table_header.append("Units")
        return table_header

    def to_table(self):
        data_table = super(Transfer, self).to_table()
        data_table.append(self.units)
        return data_table


class Dividend(Transaction):
    def __init__(self, stock, date, price, units):
        super(Dividend, self).__init__("Dividend", stock, date)
        self.units = units
        self.price = price
        self.amount = self.units * self.price

    def __str__(self):
        return "%s, %s, %s" % (super(Dividend, self).__str__(), self.units, self.price)

    @classmethod
    def to_table_header(cls):
        table_header = super(Dividend, cls).to_table_header()
        table_header.append("Price")
        table_header.append("Units")
        table_header.append("Total")
        return table_header

    def to_table(self):
        data_table = super(Dividend, self).to_table()
        data_table.append(self.price)
        data_table.append(self.units)
        data_table.append(self.price * self.units)
        return data_table


class Buy(Transaction):
    def __init__(self, stock, date, price, units, amount):
        super(Buy, self).__init__("Buy", stock, date)
        self.price = price
        self.units = units
        self.amount = amount

    def __str__(self):
        return "%s, %s, %s, %s" % (super(Buy, self).__str__(), self.units, self.price, self.amount)

    @classmethod
    def to_table_header(cls):
        table_header = super(Buy, cls).to_table_header()
        table_header.append("Price")
        table_header.append("Units")
        table_header.append("Amount")
        return table_header

    def to_table(self):
        data_table = super(Buy, self).to_table()
        data_table.append(self.price)
        data_table.append(self.units)
        data_table.append(self.amount)
        return data_table


class Sell(Transaction):
    def __init__(self, stock, date, price, units, amount):
        super(Sell, self).__init__("Sell", stock, date)
        self.price = price
        self.units = units
        self.amount = amount

    def __str__(self):
        return "%s, Units=%s, Price=%s, Amount=%s" % (super(Sell, self).__str__(), self.units, self.price, self.amount)


class Split(Transaction):
    def __init__(self, stock, date, units):
        super(Split, self).__init__("Split", stock, date)
        self.units = units
        self.price = 0.0

    def __str__(self):
        return "%s, %s, %s" % (super(Split, self).__str__(), self.units, self.price)

    @classmethod
    def to_table_header(cls):
        return ["Stock", "Date", "Units"]

    def to_table(self):
        return [self.stock, self.date, self.units]


class Deposit(Transaction):
    def __init__(self, date, amount):
        super(Deposit, self).__init__("Deposit", None, date)
        self.amount = amount

    def __str__(self):
        return "%s, %s" % (super(Deposit, self).__str__(), self.amount)


class Withdrawal(Transaction):
    def __init__(self, date, amount):
        super(Withdrawal, self).__init__("Withdrawal", None, date)
        self.amount = amount

    def __str__(self):
        return "%s, %s" % (super(Withdrawal, self).__str__(), self.amount)


class Tax(Transaction):
    def __init__(self, date, amount):
        super(Tax, self).__init__("Tax", None, date)
        self.amount = amount

    def __str__(self):
        return "%s, %s" % (super(Tax, self).__str__(), self.amount)
