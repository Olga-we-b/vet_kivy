class Service:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def change_price(self, price):
        self.price = price
