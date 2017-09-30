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

    def test_add_item_to_shoppinglist_is_successful(self):
        num_items = len(self.shoppinglist.items)
        self.assertTrue(self.shoppinglist.add_item("abc457", "cabbages", "5,000/=", "4"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 1)
        self.assertTrue(self.shoppinglist.add_item("cdc671", "carrots", "3,00/=", "5"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 2)

    def test_add_item_to_shoppinglist_fails_if_item_name_already_exists(self):
        num_items = len(self.shoppinglist.items)
        self.assertTrue(self.shoppinglist.add_item("abc457", "cabbages", "5,000/=", "4"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 1)
        self.assertFalse(self.shoppinglist.add_item("cdc671", "cabbages", "3,00/=", "5"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 1)

    def test_remove_item_fails_if_item_id_is_not_in_shoppinglist(self):
        num_items = len(self.shoppinglist.items)
        self.assertTrue(self.shoppinglist.add_item("abc457", "cabbages", "5,000/=", "4"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 1)
        self.assertFalse(self.shoppinglist.remove_item("34e"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 1)

    def test_remove_item_is_successful(self):
        num_items = len(self.shoppinglist.items)
        self.assertTrue(self.shoppinglist.add_item("abc457", "cabbages", "5,000/=", "4"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 1)
        self.assertTrue(self.shoppinglist.add_item("cdc671", "carrots", "3,00/=", "5"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 2)
        self.assertTrue(self.shoppinglist.remove_item("abc457"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 1)

    def test_edit_item_fails_if_item_id_is_unknown(self):
        num_items = len(self.shoppinglist.items)
        self.assertTrue(self.shoppinglist.add_item("abc457", "cabbages", "5,000/=", "4"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 1)
        self.assertTrue(self.shoppinglist.add_item("cdc671", "carrots", "3,000/=", "5"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 2)
        self.assertFalse(self.shoppinglist.edit_item("cdc672", "green pepper", "2000", "6"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 2)

        item = self.shoppinglist.items[self.shoppinglist.id_names["cdc671"]]
        self.assertEqual(item.name, "Carrots", "Name is 'Green Pepper' and must be title-cased")
        self.assertEqual(item.price, "3,000/=")
        self.assertEqual(item.quantity, "5")

    def test_edit_item_is_successful(self):
        num_items = len(self.shoppinglist.items)
        self.assertTrue(self.shoppinglist.add_item("abc457", "cabbages", "5,000/=", "4"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 1)
        self.assertTrue(self.shoppinglist.edit_item("abc457", "carrots", "2,000/=", "5"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 1)

        edited_item = self.shoppinglist.items[self.shoppinglist.id_names["abc457"]]
        self.assertIsNotNone(edited_item)
        self.assertEqual(edited_item.name, "Carrots")
        self.assertEqual(edited_item.quantity, "5")
        self.assertEqual(edited_item.price, "2,000/=")

    def test_edit_item_fails_when_new_item_name_is_already_in_the_list(self):
        num_items = len(self.shoppinglist.items)
        self.assertTrue(self.shoppinglist.add_item("abc457", "cabbages", "5,000/=", "4"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 1)
        self.assertTrue(self.shoppinglist.add_item("cdc671", "carrots", "3,00/=", "5"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 2)
        self.assertTrue(self.shoppinglist.add_item("tad812", "green pepper", "2000", "6"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 3)
        self.assertFalse(self.shoppinglist.edit_item("tad812", "carrots", "4000", "15"))

    def test_get_item_fails_when_item_id_is_unknown(self):
        self.assertIsNone(self.shoppinglist.get_item("abc431"))
        self.assertEqual(len(self.shoppinglist.items), 0)

    def test_get_item_is_successful_for_a_known_id(self):
        num_items = len(self.shoppinglist.items)
        self.assertTrue(self.shoppinglist.add_item("abc457", "cabbages", "5,000/=", "4"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 1)
        self.assertTrue(self.shoppinglist.add_item("cdc671", "carrots", "3,00/=", "5"))
        self.assertEqual(len(self.shoppinglist.items), num_items + 2)
        item = self.shoppinglist.get_item("cdc671")
        self.assertIsNotNone(item)
        self.assertEqual(item.name, "Carrots")
        self.assertEqual(item.price, "3,00/=")
        self.assertEqual(item.quantity, "5")
