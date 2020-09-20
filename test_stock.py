from unittest import TestCase

from stock import Stock


class TestStock(TestCase):
    stock = Stock(key='O', name='Realty Income', currency='USD')
    fund = Stock(key='AVZ-ZRO', name='Avanza Zero', currency='SEK', is_stock=0)

    def test_0_get_total_price(self):
        self.assertEqual(self.stock.get_total_price(), 0)

    def test_0_get_total_price(self):
        self.assertEqual(self.stock.get_total_price(), 0)
