from datetime import datetime
from shoppinglist.models.item import Item


class ShoppingList:
    def __init__(self, list_id, name, notify_date):
        self.id = list_id
        self.name = name.title()
        self.notify_date = notify_date
        self.date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.date_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.items = dict()
        self.id_names = dict()

    def add_item(self, item_id, item_name, price, quantity):
        if item_name.title() in self.items:
            print("Item is already on the list")
            return False
        new_item = Item(item_id, item_name, price, quantity)
        self.items[new_item.name] = new_item
        self.id_names[item_id] = new_item.name
        self.date_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return True

    def remove_item(self, item_id):
        if item_id not in self.id_names:
            print(f"item with id '{item_id}' cannot be found")
            return False
        name = self.id_names[item_id]
        del self.id_names[item_id]
        del self.items[name]
        self.date_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return True
