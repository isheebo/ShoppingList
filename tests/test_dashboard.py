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

    def test_login_fails_if_email_is_not_registered(self):
        self.assertFalse(self.dashboard.login("tester@gmail.com", "testersPassword"))

    def test_login_fails_if_email_is_registered_but_password_is_wrong(self):
        self.assertEqual(len(self.dashboard.registry), 0)
        self.assertTrue(self.dashboard.signup("testing tester", "tester@gmail.com", "testersPassword"))
        self.assertEqual(len(self.dashboard.registry), 1)
        self.assertIsNotNone(self.dashboard.registry["tester@gmail.com"])
        self.assertFalse(self.dashboard.login("tester@gmail.com", "password"))

    def test_login_is_successful_for_a_known_password_and_email(self):
        self.assertEqual(len(self.dashboard.registry), 0)
        self.assertTrue(self.dashboard.signup("testing tester", "tester@gmail.com", "testersPassword"))
        self.assertEqual(len(self.dashboard.registry), 1)
        self.assertIsNotNone(self.dashboard.registry["tester@gmail.com"])
        self.assertTrue(self.dashboard.login("tester@gmail.com", "testersPassword"))

    def test_log_out_fails_if_user_is_not_logged_in(self):
        self.assertFalse(self.dashboard.logout())

    def test_log_out_is_successful_if_user_was_originally_logged_in(self):
        self.dashboard.is_logged_in = True
        self.assertTrue(self.dashboard.logout())
