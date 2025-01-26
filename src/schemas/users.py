from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional


# Схема користувача
class User(BaseModel):
    id: int
    username: str
    email: str
    avatar: str | None = None

    model_config = ConfigDict(from_attributes=True)

# Схема для запиту реєстрації
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# Схема для токену
class Token(BaseModel):
    access_token: str
    token_type: str


class RequestEmail(BaseModel):
    email: str
