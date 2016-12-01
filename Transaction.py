# -*- coding: utf-8 -*-
__author__ = 'daniel'


class Transaction(object):
    def __init__(self, stock, date):
        self.stock = stock
        self.date = date
        self.price = 0.0
        self.fee = 0.0

    def __str__(self):
        return "%s, %s" % (self.date, self.stock )



    @classmethod
    def to_table_header(cls):
        return ["Stock", "Date"]

    def to_table(self):
        return [self.stock, self.date]

    def to_csv(self):
        return ",".join(self.to_table())

class Transfer(Transaction):
    def __init__(self, stock, date, units):
        super(Transfer, self).__init__(stock, date)
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
        super(Dividend, self).__init__(stock, date)
        self.units = units
        self.price = price

    def __str__(self):
        return "%s, %s, %s, %s" % (super(Dividend, self).__str__(), "Dividend", self.units, self.price)

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
        data_table.append(self.price*self.units)
        return data_table

class Buy(Transaction):
    def __init__(self, stock, date, price, units, fee):
        super(Buy, self).__init__(stock, date)
        self.price = price
        self.units = units
        self.fee = fee

    def __str__(self):
        return "%s, %s, %s, %s, %s" % (super(Buy, self).__str__(), "Buy", self.units, self.price, self.fee)


    @classmethod
    def to_table_header(cls):
        table_header = super(Buy, cls).to_table_header()
        table_header.append("Price")
        table_header.append("Units")
        table_header.append("Fee")
        return table_header

    def to_table(self):
        data_table = super(Buy, self).to_table()
        data_table.append(self.price)
        data_table.append(self.units)
        data_table.append(self.fee)
        return data_table

class Sell(Transaction):
    def __init__(self, stock, date, price, units, fee):
        super(Sell, self).__init__(stock, date)
        self.price = price
        self.units = units
        self.fee = fee

    def __str__(self):
        return "%s, %s, %s, %s, %s" % (super(Sell, self).__str__(), "Sell", self.units, self.price, self.fee)


class Split(Transaction):
    def __init__(self, stock, date, units):
        super(Split, self).__init__(stock, date)
        self.units = units
        self.price = 0.0

    def __str__(self):
        return "%s, %s, %s, %s" % (super(Split, self).__str__(), "Split", self.units, self.price)

    @classmethod
    def to_table_header(cls):
        return ["Stock", "Date", "Units"]

    def to_table(self):
        return [self.stock, self.date, self.units]

