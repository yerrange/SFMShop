import database.connection as db
import psycopg2


conn = db.connect_to_db()

try:
    try:
        db.add_product(conn, 'Ноутбук', 50000.00, 10, 3)
        db.add_product(conn, 'Мышь', 1500.00, 20, 4)
    except psycopg2.errors.UniqueViolation:
        print('Товар с таким id уже есть в таблице')

    print("Все товары:")
    for product in db.get_all_products(conn):
        print(product)

    db.update_product_price(conn, 3, 45000.00)


finally:
    conn.close()
