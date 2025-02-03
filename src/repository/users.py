from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.schemas.users import UserCreate
from typing import Optional


class UserRepository:
    """
    Репозиторій для роботи з користувачами у базі даних.
    """

    def __init__(self, session: AsyncSession):
        """
        Ініціалізація UserRepository.

        Args:
            session (AsyncSession): Асинхронна сесія для взаємодії з базою даних.
        """
        self.db = session

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Отримання користувача за його ідентифікатором.

        Args:
            user_id (int): ID користувача.

        Returns:
            Optional[User]: Об'єкт користувача або None, якщо користувача не знайдено.
        """
        stmt = select(User).filter_by(id=user_id)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Отримання користувача за його іменем користувача.

        Args:
            username (str): Ім'я користувача.

        Returns:
            Optional[User]: Об'єкт користувача або None, якщо користувача не знайдено.
        """
        stmt = select(User).filter_by(username=username)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Отримання користувача за його email.

        Args:
            email (str): Email користувача.

        Returns:
            Optional[User]: Об'єкт користувача або None, якщо користувача не знайдено.
        """
        stmt = select(User).filter_by(email=email)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def create_user(self, body: UserCreate, avatar: Optional[str] = None) -> User:
        """
        Створення нового користувача.

        Args:
            body (UserCreate): Дані нового користувача.
            avatar (Optional[str]): URL аватару користувача (необов'язковий параметр).

        Returns:
            User: Створений об'єкт користувача.
        """
        user = User(
            **body.model_dump(exclude_unset=True, exclude={"password"}),
            hashed_password=body.password,
            avatar=avatar
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def confirmed_email(self, email: str) -> None:
        """
        Підтвердження email користувача.

        Args:
            email (str): Email користувача.

        Returns:
            None
        """
        user = await self.get_user_by_email(email)
        if user:
            user.confirmed = True
            await self.db.commit()

    async def update_user(self, user: User) -> None:
        """
        Оновлення даних користувача.

        Args:
            user (User): Об'єкт користувача, який потрібно оновити.

        Returns:
            None
        """
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
