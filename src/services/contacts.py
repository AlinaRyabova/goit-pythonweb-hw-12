

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import date, timedelta
from src.database.models import Contact
from src.schemas.contacts import ContactBase, ContactResponse
from src.database.models import User
from typing import List, Optional

class ContactService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Пошук контактів за параметрами (ім'я, прізвище, email)
    async def search_contacts(
        self, first_name: Optional[str], last_name: Optional[str], email: Optional[str], skip: int = 0, limit: int = 100
    ) -> List[ContactResponse]:
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

    # Отримання контактів з днями народження на найближчі 7 днів
    async def get_upcoming_birthdays(self, days: int = 7) -> List[ContactResponse]:
        today = date.today()
        end_date = today + timedelta(days=days)
        query = select(Contact).filter(
        Contact.birthday.between(today, end_date)
    )
        result = await self.db.execute(query)
        contacts = result.scalars().all()
        return [ContactResponse.from_orm(contact) for contact in contacts]


    async def get_contacts(self, user: User, skip: int = 0, limit: int = 100) -> List[ContactResponse]:
        query = select(Contact).offset(skip).limit(limit)
        result = await self.db.execute(query)
        contacts = result.scalars().all()
        return [ContactResponse.from_orm(contact) for contact in contacts]

    async def get_contact_by_id(self, contact_id: int) -> Optional[ContactResponse]:
        query = select(Contact).filter(Contact.id == contact_id)
        result = await self.db.execute(query)
        contact = result.scalar_one_or_none()
        if contact:
            return ContactResponse.from_orm(contact)
        return None

    async def create_contact(self, contact_data: ContactBase) -> ContactResponse:
        contact = Contact(**contact_data.dict())
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return ContactResponse.from_orm(contact)

    async def update_contact(self, contact_id: int, contact_data: ContactBase) -> Optional[ContactResponse]:
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
        query = select(Contact).filter(Contact.id == contact_id)
        result = await self.db.execute(query)
        contact = result.scalar_one_or_none()
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
            return ContactResponse.from_orm(contact)
        return None
