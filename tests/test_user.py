import unittest
from passlib.apps import custom_app_context as pwd_context
from shoppinglist.models.user import User
from shoppinglist.models.shoppinglist import ShoppingList


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User("Alan Jackson", "jacko@gmail.com", "living-on-love")

    def test_user_is_created_successfully(self):
        self.assertIsNotNone(self.user)
        self.assertEqual(self.user.name, "Alan Jackson")
        self.assertEqual(self.user.email, "jacko@gmail.com")
        self.assertTrue(pwd_context.verify("living-on-love", self.user.password))

    def test_create_shoppinglist_fails_if_name_already_exists(self):
        self.user.shoppinglists = dict(Groceries=ShoppingList("x2x2x2", "groceries", "17/02/2018"))
        num_lists = len(self.user.shoppinglists)
        self.assertFalse(self.user.create_shoppinglist("gh231a", "groceries", "5/12/2017"))
        self.assertEqual(len(self.user.shoppinglists), num_lists)

    def test_create_shoppinglist_is_successful(self):
        num_lists = len(self.user.shoppinglists)
        self.assertTrue(self.user.create_shoppinglist("gh231a", "groceries", "5/12/2017"))
        self.assertEqual(len(self.user.shoppinglists), num_lists + 1)
        self.assertTrue(self.user.create_shoppinglist("far712", "furniture", "12-12-2018"))
        self.assertEqual(len(self.user.shoppinglists), num_lists + 2)

    def test_delete_fails_if_list_id_is_unknown(self):
        num_lists = len(self.user.shoppinglists)
        self.assertFalse(self.user.delete_shoppinglist("gh231a"))
        self.assertEqual(len(self.user.shoppinglists), num_lists)

    def test_delete_list_is_successful(self):
        num_lists = len(self.user.shoppinglists)
        self.assertTrue(self.user.create_shoppinglist("gh231a", "groceries", "5/12/2017"))
        self.assertEqual(len(self.user.shoppinglists), num_lists + 1)
        self.assertTrue(self.user.create_shoppinglist("far712", "furniture", "12-12-2018"))
        self.assertEqual(len(self.user.shoppinglists), num_lists + 2)
        self.assertTrue(self.user.delete_shoppinglist("gh231a"))
        self.assertEqual(len(self.user.shoppinglists), num_lists + 1)
        self.assertEqual(len(self.user.ids_names), num_lists + 1)

    def test_edit_list_fails_if_list_id_is_unknown(self):
        num_lists = len(self.user.shoppinglists)
        self.assertFalse(self.user.edit_shoppinglist("gh231a", "bla bla", "12-03-2018"))
        self.assertEqual(len(self.user.shoppinglists), num_lists)

    def test_edit_fails_if_new_name_is_name_of_already_existing_list(self):
        num_lists = len(self.user.shoppinglists)
        self.assertTrue(self.user.create_shoppinglist("gh231a", "groceries", "5/12/2017"))
        self.assertEqual(len(self.user.shoppinglists), num_lists + 1)
        self.assertTrue(self.user.create_shoppinglist("far712", "furniture", "12-12-2018"))
        self.assertEqual(len(self.user.shoppinglists), num_lists + 2)
        self.assertFalse(self.user.edit_shoppinglist("far712", "groceries", "04-05-2019"))
        self.assertEqual(len(self.user.shoppinglists), num_lists + 2)
        __list = self.user.shoppinglists[self.user.ids_names["far712"]]
        self.assertEqual(__list.name, "Furniture")
        self.assertEqual(__list.notify_date, "12-12-2018")

    def test_edit_list_is_successful_for_a_known_id(self):
        num_lists = len(self.user.shoppinglists)
        self.assertTrue(self.user.create_shoppinglist("gh231a", "groceries", "5/12/2017"))
        self.assertEqual(len(self.user.shoppinglists), num_lists + 1)
        self.assertTrue(self.user.create_shoppinglist("far712", "furniture", "12-12-2018"))
        self.assertEqual(len(self.user.shoppinglists), num_lists + 2)
        self.assertTrue(self.user.edit_shoppinglist("far712", "computers", "04-05-2019"))
        self.assertEqual(len(self.user.shoppinglists), num_lists + 2)  # to be sure that a new list is not created
        __list = self.user.shoppinglists[self.user.ids_names["far712"]]
        self.assertEqual(__list.name, "Computers")
        self.assertEqual(__list.notify_date, "04-05-2019")
