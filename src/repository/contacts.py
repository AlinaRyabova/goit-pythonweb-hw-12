from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas.contacts import ContactBase
from src.database.models import User


class ContactRepository:
    """
    Репозиторій для роботи з контактами у базі даних.
    """

    def __init__(self, session: AsyncSession):
        """
        Ініціалізація ContactRepository.

        Args:
            session (AsyncSession): Асинхронна сесія для взаємодії з базою даних.
        """
        self.db = session

    async def get_contacts(self, user: User, skip: int, limit: int) -> List[Contact]:
        """
        Отримання списку контактів користувача з пагінацією.

        Args:
            user (User): Об'єкт користувача.
            skip (int): Кількість пропущених записів (offset).
            limit (int): Максимальна кількість контактів для вибірки.

        Returns:
            List[Contact]: Список контактів.
        """
        stmt = select(Contact).filter_by(user=user).offset(skip).limit(limit)
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> Optional[Contact]:
        """
        Отримання контакту за його ідентифікатором.

        Args:
            contact_id (int): ID контакту.

        Returns:
            Optional[Contact]: Об'єкт контакту або None, якщо контакт не знайдено.
        """
        stmt = select(Contact).filter_by(id=contact_id)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactBase) -> Contact:
        """
        Створення нового контакту.

        Args:
            body (ContactBase): Дані нового контакту.

        Returns:
            Contact: Створений об'єкт контакту.
        """
        contact = Contact(**body.model_dump(exclude_unset=True))
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int) -> Optional[Contact]:
        """
        Видалення контакту за його ID.

        Args:
            contact_id (int): ID контакту.

        Returns:
            Optional[Contact]: Видалений контакт або None, якщо контакт не знайдено.
        """
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def update_contact(self, contact_id: int, body: ContactBase) -> Optional[Contact]:
        """
        Оновлення даних контакту.

        Args:
            contact_id (int): ID контакту, який потрібно оновити.
            body (ContactBase): Нові дані для оновлення.

        Returns:
            Optional[Contact]: Оновлений контакт або None, якщо контакт не знайдено.
        """
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            for key, value in body.dict(exclude_unset=True).items():
                setattr(contact, key, value)

            await self.db.commit()
            await self.db.refresh(contact)

        return contact
