from datetime import datetime, timedelta, UTC
from typing import Optional

from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from src.database.db import get_db
from src.conf.config import settings
from src.services.users import UserService
import json





class Hash:
    """
    Клас для роботи з хешуванням паролів.
    Використовує bcrypt для безпечного збереження паролів.
    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Перевіряє, чи співпадає введений пароль із хешованим паролем.

        Args:
            plain_password (str): Звичайний пароль, який потрібно перевірити.
            hashed_password (str): Хешований пароль, збережений у базі даних.

        Returns:
            bool: True, якщо паролі співпадають, інакше False.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Хешує пароль перед його збереженням.

        Args:
            password (str): Пароль користувача.

        Returns:
            str: Хешований пароль.
        """
        return self.pwd_context.hash(password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    """
    Генерує JWT токен доступу.

    Args:
        data (dict): Дані для кодування в токені.
        expires_delta (Optional[int]): Час життя токена у секундах (опціонально).

    Returns:
        str: Згенерований JWT токен.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now(UTC) + timedelta(seconds=settings.JWT_EXPIRATION_SECONDS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Отримує поточного користувача з токена доступу.

    Args:
        token (str): JWT токен, що передається у запиті.
        db (Session): Сесія бази даних SQLAlchemy.

    Returns:
        User: Об'єкт користувача, якщо аутентифікація пройшла успішно.

    Raises:
        HTTPException: Якщо токен недійсний або користувача не знайдено.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Декодування JWT токена
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        username = payload["sub"]
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_service = UserService(db)
    user = await user_service.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user


def create_email_token(data: dict) -> str:
    """
    Генерує JWT токен для підтвердження електронної пошти.

    Args:
        data (dict): Дані для кодування у токені.

    Returns:
        str: JWT токен для підтвердження email.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=7)
    to_encode.update({"iat": datetime.now(UTC), "exp": expire})
    token = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


async def get_email_from_token(token: str) -> str:
    """
    Витягує email з токена підтвердження.

    Args:
        token (str): JWT токен.

    Returns:
        str: Email користувача, якщо токен валідний.

    Raises:
        HTTPException: Якщо токен недійсний або прострочений.
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        email = payload["sub"]
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Неправильний токен для перевірки електронної пошти",
        )



