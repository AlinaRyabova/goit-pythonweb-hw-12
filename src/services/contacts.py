from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import date, timedelta
from src.database.models import Contact
from src.schemas.contacts import ContactBase, ContactResponse
from src.database.models import User
from typing import List, Optional


class ContactService:
    """
    Сервіс для управління контактами користувачів у базі даних.
    """

    def __init__(self, db: AsyncSession):
        """
        Ініціалізує сервіс контактів.

        Args:
            db (AsyncSession): Асинхронна сесія бази даних SQLAlchemy.
        """
        self.db = db

    async def search_contacts(
        self,
        first_name: Optional[str],
        last_name: Optional[str],
        email: Optional[str],
        skip: int = 0,
        limit: int = 100,
    ) -> List[ContactResponse]:
        """
        Пошук контактів за ім'ям, прізвищем або email.

        Args:
            first_name (Optional[str]): Ім'я контакту для пошуку (частковий збіг).
            last_name (Optional[str]): Прізвище контакту для пошуку (частковий збіг).
            email (Optional[str]): Email контакту для пошуку (частковий збіг).
            skip (int, optional): Кількість пропущених записів. За замовчуванням 0.
            limit (int, optional): Максимальна кількість контактів у відповіді. За замовчуванням 100.

        Returns:
            List[ContactResponse]: Список знайдених контактів.
        """
        query = select(Contact).offset(skip).limit(limit)

        if first_name:
            query = query.where(Contact.first_name.ilike(f"%{first_name}%"))
        if last_name:
            query = query.where(Contact.last_name.ilike(f"%{last_name}%"))
        if email:
            query = query.where(Contact.email.ilike(f"%{email}%"))

        result = await self.db.execute(query)
        contacts = result.scalars().all()
        return [ContactResponse.from_orm(contact) for contact in contacts]

    async def get_upcoming_birthdays(self, days: int = 7) -> List[ContactResponse]:
        """
        Отримує список контактів, які мають день народження протягом заданої кількості днів.

        Args:
            days (int, optional): Кількість днів, у межах яких слід шукати дні народження. За замовчуванням 7.

        Returns:
            List[ContactResponse]: Список контактів з днями народження у вказаний період.
        """
        today = date.today()
        end_date = today + timedelta(days=days)
        query = select(Contact).filter(Contact.birthday.between(today, end_date))

        result = await self.db.execute(query)
        contacts = result.scalars().all()
        return [ContactResponse.from_orm(contact) for contact in contacts]

    async def get_contacts(
        self, user: User, skip: int = 0, limit: int = 100
    ) -> List[ContactResponse]:
        """
        Отримує список контактів користувача.

        Args:
            user (User): Користувач, для якого отримуються контакти.
            skip (int, optional): Кількість пропущених записів. За замовчуванням 0.
            limit (int, optional): Максимальна кількість контактів у відповіді. За замовчуванням 100.

        Returns:
            List[ContactResponse]: Список контактів користувача.
        """
        query = select(Contact).offset(skip).limit(limit)
        result = await self.db.execute(query)
        contacts = result.scalars().all()
        return [ContactResponse.from_orm(contact) for contact in contacts]

    async def get_contact_by_id(self, contact_id: int) -> Optional[ContactResponse]:
        """
        Отримує контакт за його ідентифікатором.

        Args:
            contact_id (int): Ідентифікатор контакту.

        Returns:
            Optional[ContactResponse]: Об'єкт контакту, якщо знайдено, інакше None.
        """
        query = select(Contact).filter(Contact.id == contact_id)
        result = await self.db.execute(query)
        contact = result.scalar_one_or_none()
        if contact:
            return ContactResponse.from_orm(contact)
        return None

    async def create_contact(self, contact_data: ContactBase) -> ContactResponse:
        """
        Створює новий контакт.

        Args:
            contact_data (ContactBase): Дані для створення нового контакту.

        Returns:
            ContactResponse: Створений контакт.
        """
        contact = Contact(**contact_data.dict())
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return ContactResponse.from_orm(contact)

    async def update_contact(
        self, contact_id: int, contact_data: ContactBase
    ) -> Optional[ContactResponse]:
        """
        Оновлює існуючий контакт за ідентифікатором.

        Args:
            contact_id (int): Ідентифікатор контакту.
            contact_data (ContactBase): Нові дані для оновлення контакту.

        Returns:
            Optional[ContactResponse]: Оновлений контакт або None, якщо не знайдено.
        """
        query = select(Contact).filter(Contact.id == contact_id)
        result = await self.db.execute(query)
        contact = result.scalar_one_or_none()
        if contact:
            for field, value in contact_data.dict(exclude_unset=True).items():
                setattr(contact, field, value)
            await self.db.commit()
            await self.db.refresh(contact)
            return ContactResponse.from_orm(contact)
        return None

    async def remove_contact(self, contact_id: int) -> Optional[ContactResponse]:
        """
        Видаляє контакт за ідентифікатором.

        Args:
            contact_id (int): Ідентифікатор контакту для видалення.

        Returns:
            Optional[ContactResponse]: Видалений контакт або None, якщо не знайдено.
        """
        query = select(Contact).filter(Contact.id == contact_id)
        result = await self.db.execute(query)
        contact = result.scalar_one_or_none()
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
            return ContactResponse.from_orm(contact)
        return None
