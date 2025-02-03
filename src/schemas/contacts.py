from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class ContactBase(BaseModel):
    """
    Базова схема для створення контакту.

    Атрибути:
        first_name (str): Ім'я контакту.
        last_name (str): Прізвище контакту.
        email (str): Email-адреса контакту.
        phone_number (str): Номер телефону контакту.
        birthday (date): Дата народження контакту.
        additional_info (Optional[str]): Додаткова інформація (необов'язковий параметр).
    """

    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
    additional_info: Optional[str] = None

    class Config:
        from_attributes = True


class ContactResponse(BaseModel):
    """
    Схема відповіді для контакту.

    Атрибути:
        id (Optional[int]): Унікальний ідентифікатор контакту.
        first_name (str): Ім'я контакту.
        last_name (str): Прізвище контакту.
        email (str): Email-адреса контакту.
        created_at (datetime): Дата і час створення контакту.
        phone_number (Optional[str]): Номер телефону контакту.
    """

    id: Optional[int]
    first_name: str
    last_name: str
    email: str
    created_at: datetime
    phone_number: Optional[str]

    class Config:
        from_attributes = True
