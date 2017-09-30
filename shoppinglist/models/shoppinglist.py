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
