from src.utils.calculations import (
    calculate_discount,
    calculate_delivery,
    calculate_final_price
)

from src.utils.validators import (
    validate_age,
    validate_email
)


if __name__ == '__main__':
    age = 20
    email = "ivan@test.com"

    if validate_age(age) and validate_email(email):
        print('Возраст валиден: True')
        print('Email валиден: True')
        price, discount, weight = 1000, 0.1, 5
        final_price = calculate_final_price(
            price,
            calculate_discount(price, discount),
            calculate_delivery(5)
        )
        print('Итоговая стоимость заказа:', final_price)
    else:
        print('Возраст или email невалидные')
