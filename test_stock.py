from unittest import TestCase
from stock import Stock
from unittest import TestCase

from stock import Stock


class TestStock(TestCase):
    key = 'O'
    name = 'Realty Income'
    currency = 'USD'
    stock = Stock(key=key, name=name, currency=currency)

    def test__get_fund_price(self):
        self.assertTrue(True)
