import psycopg2


def get_orders_with_products(conn, user_id):
    """Получить заказы пользователя с товарами"""
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT "
                "orders.id, products.name, "
                "order_items.quantity, order_items.price "
                "FROM orders "
                "INNER JOIN order_items ON orders.id = products.order_id "
                "INNER JOIN products ON order_items.product_id = products.id "
                "WHERE orders.user_id = %s;",
                (user_id, )
            )
            orders = cursor.fetchall()
            return orders


def get_order_statistics(conn):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT "
                "users.id, "
                "users.name,"
                "COUNT(orders.id) as order_count,"
                "COALESCE(SUM(orders.total), 0) as total_sum "
                "FROM users "
                "LEFT JOIN orders ON users.id = orders.user_id "
                "GROUP BY users.id, users.name "
                "ORDER BY total_sum DESC;"
            )
            order_statistics = cursor.fetchall()
            return order_statistics


def get_user_order_history(conn, user_id):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT "
                "orders.id, orders.created_at, products.name, "
                "order_items.quantity, order_items.price "
                "FROM orders "
                "INNER JOIN order_items "
                "ON orders.id = order_items.order_id"
                "INNER JOIN products "
                "ON order_items.product_id = products.id "
                "WHERE orders.user_id = %s "
                "ORDER BY orders.created_at DESC;",
                (user_id, )
            )
            order_history = cursor.fetchall()
            return order_history


def get_top_products(conn, limit=5):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT "
                "products.name, "
                "SUM(order_items.quantity) AS total_sold"
                "FROM products "
                "INNER JOIN order_items "
                "ON products.id = order_items.product_id"
                "GROUP BY products.name "
                "ORDER BY total_sold DESC "
                "LIMIT %s;",
                (limit, )
            )
            top_products = cursor.fetchall()
            return top_products
