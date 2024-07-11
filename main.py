from fastapi import FastAPI, Depends
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from fastapi_users import fastapi_users, FastAPIUsers

from auth.auth import auth_backend
from auth.schemas import UserRead, UserCreate
from auth.database import User
from auth.manager import get_user_manager


app = FastAPI(
    title="Project"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"

@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"

fake_users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "user", "name": "John"},
    {"id": 3, "role": "user1", "name": "Kale"},
    {"id": 4, "role": "user2", "name": "lOal", "degree": [
        {"id": 1, "created_at": "2020-01-01t00:00:00", "type_degree": "expert"}
    ]},
]

class DegreeType(Enum): # перечисления все возможные варианты для ввода. не больше не меньше
    newbie = "newbie"
    expert = "expert"

class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] # либо нам нужно звание либо вообще None


@app.get('/users/{user_id}', response_model=List[User]) # задаем модель данных
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]


fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 2, "currency": "BTC", "side": "sell", "price": 234, "amount": 2.12},
]

# @app.get('/trades')
# def get_trades(limit: int = 1, offset: int = 0): #offset - сдвиг(пагинации), limit - ограничение на кол-во сделок
#     return fake_trades[offset:][:limit] #начнем с offset и конкретные 10
#
#
#
# fake_users2 = [
#     {"id": 1, "role": "admin", "name": "Bob"},
#     {"id": 2, "role": "user", "name": "John"},
#     {"id": 3, "role": "user1", "name": "Kale"},
# ]
#
# @app.post("/users/{user_id}")
# def change_user_name(user_id: int, new_name: str):
#     filtered_users = list(filter(lambda user: user.get("id") == user_id, fake_users2))
#     if filtered_users:
#         current_user = filtered_users[0]
#         current_user["name"] = new_name
#         return {"status": 200, "data": current_user}
#     else:
#         return {"status": 404, "message": "User not found"}
#создаем модель данных Trade
class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=20) # макс длина поля
    side: str
    price: float = Field(ge=0) #число должно быть больше или равно 0
    amount: float


@app.post("/trades", response_model=List[Trade])
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return fake_trades