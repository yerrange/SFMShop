from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi import HTTPException


app = FastAPI()

products = [
    {"id": 1, "name": "Ноутбук", "price": 50000},
    {"id": 2, "name": "Мышь", "price": 1500}
]

order_counter = 0
user_counter = 0
orders = []
users = []


@app.get("/products")
def get_products(limit: int = 10, offset: int = 0):
    return {"limit": limit, "offset": offset, "products": products[offset:limit+1]}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    else:
        raise HTTPException(status_code=404, detail="Item not found")     


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_product(order: OrderCreate):
    global order_counter
    order_counter += 1
    orders.append(
        {
            "id": order_counter,
            "user_id": order.user_id,
            "product_id": order.product_id,
            "quantity": order.quantity,
        }
    )
    return {
        "id": order_counter,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "message": "Заказ создан"
    }


@app.get("/users")
def get_users(limit: int = 10, offset: int = 0):
    return {"limit": limit, "offset": offset, "users": users[offset:limit+1]}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


class UserCreate(BaseModel):
    name: str
    email: str


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    global user_counter
    user_counter += 1
    new_user = {
        "id": user_counter,
        "name": user.name,
        "email": user.email
    }
    users.append(new_user)
    return new_user