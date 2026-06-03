import time


def calculate_discount(price, discount_rate):
    return price * discount_rate

def calculate_delivery(weight, base_cost=100):
    return base_cost + weight * 10

def calculate_final_price(price, discount, delivery):
    return price - discount + delivery


def measure_time(func):
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
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.rstrip().split() for line in file.readlines()]


def read_file_dict(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return {
            int(line.rstrip().split()[0]): line.rstrip().split()[1:]
            for line in file.readlines()
        }


print(find_product_in_list(read_file_list("products_2000_shuffled.txt"), 55))
print(find_product_in_dict(read_file_dict("products_2000_shuffled.txt"), 55))
