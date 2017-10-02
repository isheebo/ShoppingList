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

    def delete_shoppinglist(self, list_id):
        if list_id not in self.ids_names:
            print(f"List with ID '{list_id}' not found")
            return False

        print(f"'{self.ids_names[list_id]}' has been successfully deleted!")
        del self.shoppinglists[self.ids_names[list_id]]
        del self.ids_names[list_id]
        return True

    def edit_shoppinglist(self, list_id, name, notify_date):
        if list_id not in self.ids_names:
            print(f"List with ID '{list_id}' not found")
            return False  # we can't edit things that don't exist

        list_name = name.title()
        for saved_id, saved_name in self.ids_names.items():
            if saved_name == list_name and list_id != saved_id:
                return False  # duplicate names not allowed

        __list = self.shoppinglists[self.ids_names[list_id]]
        __list.name = list_name
        __list.notify_date = notify_date
        return True

    def get_shoppinglist(self, list_id):
        if list_id not in self.ids_names:
            print(f"List with ID '{list_id}' not found")
            return None
        return self.shoppinglists[self.ids_names[list_id]]
