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
                "SELECT user_id, "
                "COUNT(*) AS order_count, SUM(total) AS total_sum "
                "FROM orders "
                "GROUP BY user_id "
                "ORDER BY total_sum DESC;"
            )
            order_statistics = cursor.fetchall()
            return order_statistics
