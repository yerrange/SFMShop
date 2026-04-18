import database.connection as db
import psycopg2


# conn = db.connect_to_db()

# try:
#     try:
#         db.add_product(conn, 'Ноутбук', 50000.00, 10, 3)
#         db.add_product(conn, 'Мышь', 1500.00, 20, 4)
#     except psycopg2.errors.UniqueViolation:
#         print('Товар с таким id уже есть в таблице')

#     print("Все товары:")
#     for product in db.get_all_products(conn):
#         print(product)s

#     db.update_product_price(conn, 3, 45000.00)


# finally:
#     conn.close()


conn = db.connect_to_db()

try:
    db.create_user(conn, 'Иван', 'ivan@test.ru')
    user = db.get_user_by_id(conn, 7)
    if user:
        print(f'Пользователь найден: {user}')
    db.create_order(conn, 7, 50000.00)
    orders = db.get_user_orders(conn, 7)
    print(f'Заказы пользователя: {orders}')

finally:
    conn.close()
