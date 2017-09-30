from passlib.apps import custom_app_context as pwd_context
from shoppinglist.models.shoppinglist import ShoppingList


class User:
    """ Represents a logged-in user and the operations they can perform"""

    def __init__(self, name, email, password):
        self.name = name.title()
        self.email = email
        self.password = pwd_context.hash(password)
        self.shoppinglists = dict()  # {id:ShoppingList}
        self.ids_names = dict()  # mapping
