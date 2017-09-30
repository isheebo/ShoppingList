class Item:
    def __init__(self, item_id, name, price, quantity):
        self.id = item_id
        self.name = name.title()
        self.price = price
        self.quantity = quantity
