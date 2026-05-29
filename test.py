from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi import HTTPException
from src.database.connection import (
    connect_to_db,
    get_all_products,
    get_product_by_id,
    create_order as create_order_service,
    delete_product as delete_product_service,
    get_user_by_id,
    create_user as create_user_service,
    get_users as get_users_service,
    add_product,
    update_product as update_product_service
)
from contextlib import asynccontextmanager
from decimal import Decimal
from src.models.product import Product
from src.models.user import User
from src.models.order import Order
from fastapi.testclient import TestClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    global conn

    # startup
    conn = connect_to_db()

    yield

    # shutdown
    if conn:
        conn.close()


app = FastAPI(lifespan=lifespan)


class ProductCreate(BaseModel):
    name: str
    price: Decimal
    quantity: int


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    try:
        product = add_product(
            conn,
            product.name,
            product.price,
            product.quantity
        )
        return {
            "message": "Продукт успешно создан",
            "product": Product.create_object(product)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/products")
def list_products(limit: int = 10, offset: int = 0):
    try:
        product_objects = []
        products = get_all_products(conn)
        for value in products:
            product = Product.create_object(value)
            product_objects.append(product)
        return {
            "total": len(product_objects),
            "limit": limit,
            "offset": offset,
            "products": product_objects[offset:limit]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/products/{product_id}")
def get_product(product_id: int):
    try:
        product = get_product_by_id(conn, product_id)
        if product:
            return Product.create_object(product)
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    try:
        deleted = delete_product_service(conn, product_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Product not found")
        return f"Продукт с id {product_id} удалён"
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):
    try:
        user_obj = User.create_object(get_user_by_id(conn, order.user_id))
        if not user_obj:
            raise HTTPException(
                status_code=404,
                detail="Пользователь не найден"
            )

        product_obj = Product.create_object(
            get_product_by_id(conn, order.product_id)
        )
        if not product_obj:
            raise HTTPException(status_code=404, detail="Продукт не найден")

        order_obj = Order(user_obj.id, product_obj, order.quantity)
        order = create_order_service(conn, order_obj.user, order_obj.total)
        return {
            "message": "Заказ создан",
            "order": order
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users")
def get_users(limit: int = 10, offset: int = 0):
    try:
        user_objects = []
        users = get_users_service(conn)
        for value in users:
            user_objects.append(User.create_object(value))
        return {
            "total": len(user_objects),
            "limit": limit,
            "offset": offset,
            "users": user_objects[offset:limit+1]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}")
def get_user(user_id: int):
    try:
        user = get_user_by_id(conn, user_id)
        if user:
            return User.create_object(user)
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class UserCreate(BaseModel):
    name: str
    email: str


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    try:
        user = create_user_service(conn, user.name, user.email)
        return {
            "message": "Пользователь создан",
            "user": User.create_object(user)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ProductUpdate(BaseModel):
    name: str
    price: Decimal
    quantity: int


@app.put("/products/{product_id}")
def update_product(product: ProductUpdate, product_id: int):
    try:
        if not get_product_by_id(conn, product_id):
            raise HTTPException(status_code=404, detail="Продукт не найден")
        new_product = Product.create_object(
            update_product_service(conn, product, product_id)
        )
        return {"message": "Продукт изменён", "new_product": new_product}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def test_api():
    """Тестирование API"""

    with TestClient(app) as client:
        response = client.get("/products")
        assert response.status_code == 200, response.text
        print("GET /products: OK")

        response = client.get("/products?limit=5&offset=0")
        assert response.status_code == 200, response.text
        data = response.json()
        assert "total" in data
        assert "products" in data
        print("GET /products с пагинацией: OK")

        response = client.get("/products/1")
        assert response.status_code == 200, response.text
        print("GET /products/1: OK")

        response = client.get("/products/999")
        assert response.status_code == 404, response.text
        print("GET /products/999 (404): OK")

        response = client.post("/orders", json={
            "user_id": 1,
            "product_id": 2,
            "quantity": 1,
        })
        assert response.status_code == 201, response.text
        print("POST /orders: OK")

        response = client.put("/products/1", json={
            "name": "Ноутбук обновленный",
            "price": "45000.00",
            "quantity": 10,
        })
        assert response.status_code == 200, response.text
        print("PUT /products/1: OK")

        response = client.delete("/products/10")
        assert response.status_code == 200, response.text
        print("DELETE /products/1: OK")

    print("\nВсе тесты пройдены успешно!")


if __name__ == '__main__':
    test_api()