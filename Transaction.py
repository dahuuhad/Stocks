# -*- coding: utf-8 -*-
__author__ = 'daniel'


class Transaction(object):
    def __init__(self, stock, date):
        self.stock = stock
        self.date = date

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
        self.price = price
        self.units = units

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

class Sell(Buy):
    def __init__(self, stock, date, price, units, fee):
        super(Sell, self).__init__(stock, date, price, units, fee)



class Split(Transaction):
    def __init__(self, stock, date, units):
        super(Split, self).__init__(stock, date)
        self.units = units
        self.split_ratio = self.__get_split_ratio

    @classmethod
    def to_table_header(cls):
        return ["Stock", "Date", "Units", "Split Ration"]

    def to_table(self):
        return [self.stock, self.date, self.units, self.split_ratio]


    @property
    def __get_split_ratio(self):
        if self.stock == 'AAPL':
            return 7
        elif self.stock == 'HM':
            return 2
        elif self.stock == 'SHB':
            return 3
        elif self.stock == 'SBUX':
            return 2
        elif self.stock == 'VOLV':
            return 6
        elif self.stock == 'ERIC':
            return 0.2