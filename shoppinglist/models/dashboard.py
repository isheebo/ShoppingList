from passlib.apps import custom_app_context as pwd_context
from shoppinglist.models.user import User


class Dashboard:
    def __init__(self):
        self.registry = dict()
        self.is_logged_in = False

    def signup(self, name, email, password):
        has_been_registered = False
        user = User(name, email, password)
        if user and user.email not in self.registry:
            self.registry[user.email] = user
            has_been_registered = True
        return has_been_registered

    def login(self, email, password):
        if email not in self.registry:  # if user is not yet registered, return False
            print("login failed due to an unknown email address!")
            return False

        if pwd_context.verify(password, self.registry[email].password):
            self.is_logged_in = True
            return True
        return False

    def logout(self):
        is_logged_out = False
        if self.is_logged_in:  # for a user to logout, they must be logged in
            # notice we don't delete self.registry[email], so that once
            # someone wants to login again, they do it without needing to first signup again
            is_logged_out = True
        return is_logged_out
