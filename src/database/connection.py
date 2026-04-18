import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")


def connect_to_db():
    conn = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password
    )
    return conn


def add_product(conn, name, price, quantity, id=None):
    with conn:
        with conn.cursor() as cursor:
            if id:
                cursor.execute(
                    "INSERT INTO products (id, name, price, quantity) VALUES (%s, %s, %s, %s);",
                    (id, name, price, quantity)
                )
            else:
                cursor.execute(
                    "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s);",
                    (name, price, quantity)
                )
            conn.commit()
            print(f"Товар добавлен: {name}, {price}, {quantity}")


def get_all_products(conn):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products;")
            products = cursor.fetchall()
    return products


def update_product_price(conn, product_id, new_price):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE products SET price = %s WHERE id = %s",
                (new_price, product_id)
            )
            conn.commit()
            print(f"Цена обновлена: {new_price}")
