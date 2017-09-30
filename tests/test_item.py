import unittest
from shoppinglist.models.item import Item


class TestItem(unittest.TestCase):
    def setUp(self):
        self.item = Item("abc123", "cabbages", "5,000/=", "4")

    def test_item_is_created_successfully(self):
        self.assertIsNotNone(self.item)
        self.assertEqual(self.item.name, "Cabbages", "Name has to be 'Cabbages'")
        self.assertEqual(self.item.quantity, "4")
        self.assertEqual(self.item.id, "abc123")
        self.assertEqual(self.item.price, "5,000/=")
