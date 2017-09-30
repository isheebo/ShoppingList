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
