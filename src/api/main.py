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
    add_product
)
from contextlib import asynccontextmanager
from decimal import Decimal
from src.models.product import Product
from src.models.user import User


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


@app.post("/products")
def create_product(product: ProductCreate):
    try:
        product = add_product(conn, product.name, product.price, product.quantity)
        return {"message": "Продукт успешно создан", "product": Product.create_object(product)}
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    try:
        deleted = delete_product_service(conn, product_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Product not found")
        return f"Продукт с id {product_id} удалён"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


@app.post("/orders")
def create_order(order: OrderCreate):
    try:
        order_created = create_order_service(conn, order.user_id, order.total)
        return {
            "id": order_created[0],
            "user_id": order_created[1],
            "total": order_created[2],
            "created_at": order_created[3],
            "message": "Заказ создан"
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
        return {"total": len(user_objects), "limit": limit, "offset": offset, "users": user_objects[offset:limit+1]}
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class UserCreate(BaseModel):
    name: str
    email: str


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    try:
        user = create_user_service(conn, user.name, user.email)
        return {"message": "Пользователь создан", "user": User.create_object(user)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
