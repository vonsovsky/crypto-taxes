class Order:
    def __init__(self, currency_from, currency_to, count, unit_price, filled):
        self.currency_from = currency_from
        self.currency_to = currency_to
        self.count = count
        self.unit_price = unit_price
        self.filled = filled

    def __repr__(self):
        return f"{self.currency_from} to {self.currency_to}; " \
               f"{self.count} for {self.unit_price} at {self.filled}"
