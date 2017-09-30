from shoppinglist.models.dashboard import Dashboard
import unittest


class TestDashBoard(unittest.TestCase):
    def setUp(self):
        self.dashboard = Dashboard()

    def test_signup_is_successful(self):
        self.assertEqual(len(self.dashboard.registry), 0)
        self.assertTrue(self.dashboard.signup("testing tester", "tester@gmail.com", "testersPassword"))
        self.assertEqual(len(self.dashboard.registry), 1)
        self.assertIsNotNone(self.dashboard.registry["tester@gmail.com"])

    def test_sign_up_fails_if_email_is_already_registered(self):
        self.assertEqual(len(self.dashboard.registry), 0)
        self.assertTrue(self.dashboard.signup("testing tester", "tester@gmail.com", "testersPassword"))
        self.assertEqual(len(self.dashboard.registry), 1)
        self.assertIsNotNone(self.dashboard.registry["tester@gmail.com"])  # it has to be a User object
        self.assertFalse(self.dashboard.signup("testing tester", "tester@gmail.com", "testersPassword"))
        self.assertEqual(len(self.dashboard.registry), 1)
