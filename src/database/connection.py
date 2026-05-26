import psycopg2

def connect_to_db():
    """Подключение к базе данных PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="sfmshop",
            user="postgres",
            password="password"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

def add_product(conn, name, price, quantity):
    """Добавить товар в базу данных"""
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)",
            (name, price, quantity)
        )
        conn.commit()
        cursor.close()
        print(f"Товар '{name}' добавлен")
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении товара: {e}")
        conn.rollback()

def get_all_products(conn):
    """Получить все товары из базы данных"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        return products
    except psycopg2.Error as e:
        print(f"Ошибка при получении товаров: {e}")
        return []

def update_product_price(conn, product_id, new_price):
    """Обновить цену товара"""
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET price = %s WHERE id = %s",
            (new_price, product_id)
        )
        conn.commit()
        cursor.close()
        print(f"Цена товара с ID {product_id} обновлена")
    except psycopg2.Error as e:
        print(f"Ошибка при обновлении цены: {e}")
        conn.rollback()

def create_user(conn, name, email):
    """Создать пользователя"""
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (name, email)
        )
        conn.commit()
        cursor.close()
        print(f"Пользователь '{name}' создан")
    except psycopg2.Error as e:
        print(f"Ошибка при создании пользователя: {e}")
        conn.rollback()

def get_user_by_id(conn, user_id):
    """Получить пользователя по ID"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return {"id": user[0], "name": user[1], "email": user[2]}
        return None
    except psycopg2.Error as e:
        print(f"Ошибка при получении пользователя: {e}")
        return None

def create_order(conn, user_id, total):
    """Создать заказ"""
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (user_id, total) VALUES (%s, %s)",
            (user_id, total)
        )
        conn.commit()
        cursor.close()
        print(f"Заказ создан: user_id={user_id}, total={total}")
    except psycopg2.Error as e:
        print(f"Ошибка при создании заказа: {e}")
        conn.rollback()

def get_user_orders(conn, user_id):
    """Получить заказы пользователя"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
        orders = cursor.fetchall()
        cursor.close()
        return orders
    except psycopg2.Error as e:
        print(f"Ошибка при получении заказов: {e}")
        return []
