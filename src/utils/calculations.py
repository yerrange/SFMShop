import time
from datetime import datetime


def calculate_discount(price, discount_rate):
    return price * discount_rate

def calculate_delivery(weight, base_cost=100):
    return base_cost + weight * 10

def calculate_final_price(price, discount, delivery):
    return price - discount + delivery


def measure_time(func):
    """Замеряет время работы функции"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        stop = time.time()
        print(f'Функция отработала за {stop - start:.10f} секунд')
        return result
    return wrapper


@measure_time
def find_product_in_list(products, product_id):
    """Поиск в списке (медленный)"""
    for product in products:
        if int(product[0]) == product_id:
            return tuple(product)
    return None


@measure_time
def find_product_in_dict(products, product_id):
    """Поиск в словаре (быстрый)"""
    return (
        (product_id, products.get(product_id))
        if products.get(product_id)
        else None
    )


def read_file_list(filename):
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


def read_file_dict(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return {
            int(line.rstrip().split()[0]): line.rstrip().split()[1:]
            for line in file.readlines()
        }


# print(find_product_in_list(read_file_list("products_2000_shuffled.txt"), 55))
# print(find_product_in_dict(read_file_dict("products_2000_shuffled.txt"), 55))


@measure_time
def sort_bubble(data, key_index=0):
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


@measure_time
def sort_fast(data):
    return sorted(data, key=lambda x: x[1])


sort_bubble(read_file_list("orders_10000_unsorted.txt"))
sort_fast(read_file_list("orders_10000_unsorted.txt"))

# Функция отработала за 3,4940419197 секунд
# Функция отработала за 0,0025281906 секунд

# sort_fast отработала быстрее sort_bubble примерно в 1382 раза
# на списке из 10000 записей,
# т.к. сложность алгоритма пузырька n**2,
# а sorted (Timsort) – n log n.
