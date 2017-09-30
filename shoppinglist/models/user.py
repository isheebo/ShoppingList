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

    def create_shoppinglist(self, list_id, name, notify_date):
        if name.title() in self.shoppinglists:
            print(f"a shoppinglist with name '{name}' already exists")
            return False
        new_list = ShoppingList(list_id, name, notify_date)
        self.shoppinglists[new_list.name] = new_list
        self.ids_names[new_list.id] = new_list.name
        return True
