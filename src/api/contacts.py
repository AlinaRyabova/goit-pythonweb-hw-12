

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.schemas.contacts import ContactBase, ContactResponse
from src.services.contacts import ContactService
from src.conf import messages
from src.services.auth import get_current_user
from src.database.models import User

router = APIRouter(prefix="/contacts", tags=['contacts'])

# Оновлений маршрут для пошуку контактів за параметрами запиту
@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0,
    limit: int = 100,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user),
):
    contact_service = ContactService(db)
    contacts = await contact_service.search_contacts(first_name, last_name, email, skip, limit)
    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.CONTACT_NOT_FOUND
        )
    return contacts

# Маршрут для отримання контактів з днями народження на найближчі 7 днів
@router.get("/birthdays", response_model=List[ContactResponse])
async def get_upcoming_birthdays(
    days: int = 7,
    db: AsyncSession = Depends(get_db),
):
    contact_service = ContactService(db)
    contacts = await contact_service.get_upcoming_birthdays(days)
    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.CONTACT_NOT_FOUND
        )
    return contacts

@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    contact = await contact_service.get_contact_by_id(contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.CONTACT_NOT_FOUND
        )
    return contact

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactBase, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    return await contact_service.create_contact(body)

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactBase, contact_id: int, db: AsyncSession = Depends(get_db)
):
    contact_service = ContactService(db)
    contact = await contact_service.update_contact(contact_id, body)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.CONTACT_NOT_FOUND
        )
    return contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    contact = await contact_service.remove_contact(contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.CONTACT_NOT_FOUND
        )
    return None  # Статус 204 No Content, без тіла відповіді
