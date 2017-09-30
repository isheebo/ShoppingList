import unittest
from datetime import datetime
from shoppinglist.models.shoppinglist import ShoppingList


class TestShoppingList(unittest.TestCase):
    def setUp(self):
        self.shoppinglist = ShoppingList("cab762", "groceries", "17-10-2017")

    def test_create_shoppinglist(self):
        self.assertIsNotNone(self.shoppinglist)
        self.assertEqual(self.shoppinglist.id, "cab762")
        self.assertEqual(self.shoppinglist.name, "Groceries")
        self.assertEqual(self.shoppinglist.notify_date, "17-10-2017")
        self.assertEqual(self.shoppinglist.date_created, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(self.shoppinglist.date_modified, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))