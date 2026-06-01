class Order:

    def __init__(self, user, product, quantity):
        self.user = user
        self.product = product
        self.quantity = quantity
        self.total = self.calculate_total()

    def calculate_total(self):
        # total = 0
        # for product in self.products:
        #     total = total + product.get_total_price()
        # return total
        return self.product.price * self.quantity

    def __str__(self):
        user_name = self.user.name if hasattr(self.user, 'name') else str(self.user)
        if self.order_id:
            return 'Заказ #' + str(self.order_id) + ' на сумму ' + str(self.total) + ' руб. (Пользователь: ' + user_name + ')'
        return 'Заказ на сумму ' + str(self.total) + ' руб. (Пользователь: ' + user_name + ')'

    @classmethod
    def create_object(cls, data):
        if data:
            obj = cls(data[1], int(data[2]), int(data[3]))
            obj.id = data[0]
            return obj
        return None
