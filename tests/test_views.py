import unittest
from shoppinglist import app
from shoppinglist.views import views


class TestViews(unittest.TestCase):
    def setUp(self):
        self.test_client = app.test_client()
        self.details = dict(name="meghan taylor", email="meghan@gmail.com", password="password",
                            confirm_password="password")

    def test_get_sign_up_page_works_successfully(self):
        resp = self.test_client.get("/signup")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Already have an account?", resp.data)
        self.assertIn(b"Sign Up", resp.data)

    def test_post_to_sign_up_page_works_successfully(self):
        data = dict(name="meghan taylor", email="meghan@gmail.com", password="password", confirm_password="password")
        resp = self.test_client.post("/signup", data=data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)  # redirects to the login page

    def test_post_redirect_fails_if_one_or_all_fields_are_missing(self):
        data = dict(name="meghan taylor", email="meghan@gmail.com", password="password")
        resp = self.test_client.post("/signup", data=data)
        self.assertEqual(resp.status_code, 200)  # no redirect hence stays on the sign up page
        self.assertIn(b"Already have an account?", resp.data)
        self.assertIn(b"Sign Up", resp.data)

        # or if not fields are given....

        resp = self.test_client.post("/signup", data={})
        self.assertEqual(resp.status_code, 200)  # no redirect hence stays on the sign up page
        self.assertIn(b"Already have an account?", resp.data)
        self.assertIn(b"Sign Up", resp.data)

    def test_post_redirect_fails_if_email_is_poorly_formatted(self):
        data = dict(name="meghan taylor", email="meghan", password="password")  # with no @ in the email field
        resp = self.test_client.post("/signup", data=data)
        self.assertEqual(resp.status_code, 200)  # no redirect hence app stays on the sign up page
        self.assertIn(b"Already have an account?", resp.data)
        self.assertIn(b"Sign Up", resp.data)

    def test_post_fails_if_confirm_password_and_password_do_not_match(self):
        data = dict(name="meghan taylor", email="meghan@gmail.com", password="password", confirm_password="hello")
        resp = self.test_client.post("/signup", data=data)
        self.assertEqual(resp.status_code, 200)  # no redirect hence stays on the sign up page
        self.assertIn(b"Already have an account?", resp.data)
        self.assertIn(b"Sign Up", resp.data)

    def test_login_is_successful_for_a_registered_user(self):
        # signing up

        resp = self.test_client.post("/signup", data=self.details, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

        # logging in
        resp = self.test_client.post("/login",
                                     data=dict(email=self.details['email'], password=self.details['password']),
                                     follow_redirects=True)
        self.assertEqual(resp.status_code, 200)  # redirects to the Dashboard/home page of the app
        self.assertTrue(views.dashboard.is_logged_in)

    def test_home_page_can_be_accessed_for_a_logged_in_user(self):
        details = dict(name="meghan taylor", email="meghan@gmail.com", password="password", confirm_password="password")
        resp = self.test_client.post("/signup", data=details)
        self.assertEqual(resp.status_code, 302)
        self.assertIn(b'/login', resp.data)
        self.assertFalse(views.dashboard.is_logged_in)

        # logging in
        resp = self.test_client.post("/login", data=dict(email=details['email'], password=details['password']),
                                     follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(views.dashboard.is_logged_in)

        resp = self.test_client.post("/view/lists")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'You have no shopping lists yet!', resp.data)  # since user has not created any shoppinglists

    def test_get_home_page_redirects_to_the_log_in_page_for_an_unregistered_user(self):
        self.assertFalse(views.dashboard.is_logged_in)
        resp = self.test_client.get("/view/lists", follow_redirects=True)
        self.assertIn(b'<h2 class="text-capitalize card-title">Sign In</h2>', resp.data)

    def test_logout(self):
        pass
