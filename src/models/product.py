from src.models.exceptions import NegativePriceError, InsufficientStockError, SFMShopException


class Product:

    def __init__(self, name, price, quantity):
        self.name = name
        if price < 0:
            raise NegativePriceError('Цена не может быть отрицательной')
        self.price = price
        self.quantity = quantity

    def sell(self, amount):
        if self.quantity < amount:
            raise InsufficientStockError(f'Товара недостаточно. На складе: {self.quantity}, требуется: {amount}')
        self.quantity = self.quantity - amount

    @classmethod
    def create_object(cls, data):
        obj = cls(data[1], int(data[2]), int(data[3]))
        obj.id = data[0]
        return obj
