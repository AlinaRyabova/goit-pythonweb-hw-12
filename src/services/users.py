from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.repository.users import UserRepository
from src.schemas.users import UserCreate

class UserService:
    """
    Сервіс для управління користувачами.

    Використовує UserRepository для роботи з базою даних та Gravatar для отримання аватарів.
    """

    def __init__(self, db: AsyncSession):
        """
        Ініціалізує сервіс користувачів.

        Args:
            db (AsyncSession): Асинхронна сесія бази даних.
        """
        self.repository = UserRepository(db)

    async def create_user(self, body: UserCreate):
        """
        Створює нового користувача та генерує аватар за допомогою Gravatar.

        Args:
            body (UserCreate): Дані для створення користувача.

        Returns:
            User: Створений користувач.
        """
        avatar = None
        try:
            g = Gravatar(body.email)
            avatar = g.get_image()
        except Exception as e:
            print(e)

        return await self.repository.create_user(body, avatar)

    async def get_user_by_id(self, user_id: int):
        """
        Отримує користувача за його ідентифікатором.

        Args:
            user_id (int): Ідентифікатор користувача.

        Returns:
            Optional[User]: Об'єкт користувача або None, якщо не знайдено.
        """
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str):
        """
        Отримує користувача за його ім'ям користувача.

        Args:
            username (str): Ім'я користувача.

        Returns:
            Optional[User]: Об'єкт користувача або None, якщо не знайдено.
        """
        return await self.repository.get_user_by_username(username)

    async def get_user_by_email(self, email: str):
        """
        Отримує користувача за його email.

        Args:
            email (str): Email користувача.

        Returns:
            Optional[User]: Об'єкт користувача або None, якщо не знайдено.
        """
        return await self.repository.get_user_by_email(email)

    async def confirmed_email(self, email: str) -> None:
        """
        Позначає email користувача як підтверджений.

        Args:
            email (str): Email користувача.
        """
        return await self.repository.confirmed_email(email)

    async def update_avatar(self, user_id: int, avatar_url: str):
        """
        Оновлює аватар користувача.

        Args:
            user_id (int): Ідентифікатор користувача.
            avatar_url (str): Нова URL-адреса аватара.

        Returns:
            Optional[User]: Оновлений користувач або None, якщо користувач не знайдений.
        """
        user = await self.repository.get_user_by_id(user_id)
        if user:
            user.avatar = avatar_url
            await self.repository.update_user(user)
            return user
        return None
