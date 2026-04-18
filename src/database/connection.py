import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import Error
from dotenv import load_dotenv
import os

load_dotenv()

db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")


def connect_to_db():
    try:
        conn = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password
        )
        return conn
    except Error as e:
        print(f"Ошибка подключения к БД: {e}")
        return None


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


def create_user(conn, name, email):
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (name, email) VALUES (%s, %s);",
                    (name, email)
                )
                conn.commit()
                print(f'Пользователь создан: {name}, {email}')
    except Error as e:
        print(f"Ошибка при создании пользователя: {e}")


def get_user_by_id(conn, user_id):
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE id = %s;",
                    (user_id, )
                )
                user = cursor.fetchone()
                return dict(user) if user else None
    except Error as e:
        print(f"Ошибка при получении пользователя: {e}")
        return None


def create_order(conn, user_id, total):
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO orders (user_id, total) VALUES (%s, %s);",
                    (user_id, total)
                )
                conn.commit()
                print(f'Заказ создан: {user_id=}, {total=}')
    except Error as e:
        print(f"Ошибка при создании заказа: {e}")


def get_user_orders(conn, user_id):
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM orders WHERE user_id = %s",
                    (user_id, )
                )
                orders = cursor.fetchall()
                return orders
    except Error as e:
        print(f"Ошибка при получении заказов: {e}")
        return []
