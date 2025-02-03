from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional


class User(BaseModel):
    """
    Схема для представлення користувача.

    Атрибути:
        id (int): Унікальний ідентифікатор користувача.
        username (str): Ім'я користувача.
        email (str): Email-адреса користувача.
        avatar (Optional[str]): URL-адреса аватару користувача (необов'язковий параметр).
    """

    id: int
    username: str
    email: str
    avatar: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """
    Схема для запиту реєстрації нового користувача.

    Атрибути:
        username (str): Ім'я користувача.
        email (str): Email-адреса користувача.
        password (str): Пароль користувача.
    """

    username: str
    email: str
    password: str


class Token(BaseModel):
    """
    Схема для представлення токену автентифікації.

    Атрибути:
        access_token (str): Токен доступу.
        token_type (str): Тип токену (наприклад, "Bearer").
    """

    access_token: str
    token_type: str


class RequestEmail(BaseModel):
    """
    Схема для запиту на відправлення листа електронною поштою.

    Атрибути:
        email (str): Email-адреса одержувача.
    """

    email: str
