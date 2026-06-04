def calculate_discount(price, discount_rate):
    return price * discount_rate

def calculate_delivery(weight, base_cost=100):
    return base_cost + weight * 10

def calculate_final_price(price, discount, delivery):
    return price - discount + delivery


import time
from datetime import datetime


def measure_time(func):
    """Замеряет время работы функции"""
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        stop = time.time()
        return round(stop-start, 10)
    return wrapper


def find_product_in_list(products, product_id):
    """Поиск в списке (медленный)"""
    for product in products:
        if int(product[0]) == product_id:
            return tuple(product)
    return None


def find_product_in_dict(products, product_id):
    """Поиск в словаре (быстрый)"""
    return (
        (product_id, products.get(product_id))
        if products.get(product_id)
        else None
    )


def read_file_list_orders(filename):
    """Читает файл с заказами"""
    with open(filename, 'r', encoding='utf-8') as file:
        return [
            [
                int(line.rstrip().split()[0]),
                datetime.strptime(line.rstrip().split()[1], "%Y-%m-%d"),
                float(line.rstrip().split()[2])
            ]
            for line in file.readlines()
        ]


def read_file_list_products(filename) -> list:
    """Читает файл с продуктами"""
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.rstrip().split() for line in file.readlines()]


def read_file_dict(filename) -> dict:
    """Читает файл с продуктами"""
    with open(filename, 'r', encoding='utf-8') as file:
        return {
            int(line.rstrip().split()[0]): line.rstrip().split()[1:]
            for line in file.readlines()
        }


# print(find_product_in_list(read_file_list("products_2000_shuffled.txt"), 55))
# print(find_product_in_dict(read_file_dict("products_2000_shuffled.txt"), 55))


def sort_bubble(data, key_index=0):
    """Медленная сортировка"""
    n = len(data)

    for i in range(n - 1):
        swapped = False

        for j in range(n - 1 - i):
            if data[j][key_index] > data[j + 1][key_index]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True

        if not swapped:
            break

    return data


def sort_fast(data):
    """Быстрая сортировка"""
    return sorted(data, key=lambda x: x[1])


# sort_bubble(read_file_list("orders_10000_unsorted.txt"))
# sort_fast(read_file_list("orders_10000_unsorted.txt"))


def compare_functions_speed(func_1, func_2):
    """Сравнивает скорость работы функций"""
    test_1 = measure_time(func_1[0])(*func_1[1])
    test_2 = measure_time(func_2[0])(*func_2[1])
    speedup = test_1 - test_2
    return round(test_1 / test_2 if speedup > 0 else 0, 2)


if __name__ == "__main__":
    print(
        "Оптимизированная функция сортировки отработала быстрее в",
        compare_functions_speed(
            (sort_bubble, (read_file_list_orders("orders_10000_unsorted.txt"), )),
            (sort_fast, (read_file_list_orders("orders_10000_unsorted.txt"), ))
        ),
        "раз"
    )

    print(
        "Оптимизированная функция поиска отработала быстрее в",
        compare_functions_speed(
            (find_product_in_list, (read_file_list_products("products_2000_shuffled.txt"), 55)),
            (find_product_in_dict, (read_file_dict("products_2000_shuffled.txt"), 55))
        ),
        "раз"
    )



# Функция отработала за 3,4940419197 секунд
# Функция отработала за 0,0025281906 секунд

# sort_fast отработала быстрее sort_bubble примерно в 1382 раза
# на списке из 10000 записей,
# т.к. сложность алгоритма пузырька n**2,
# а sorted (Timsort) – n log n.

