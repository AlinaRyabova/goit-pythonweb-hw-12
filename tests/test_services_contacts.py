import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime,timedelta
from src.database.models import Contact
from src.schemas.contacts import ContactResponse, ContactBase
from src.services.contacts import ContactService

@pytest.mark.asyncio
async def test_search_contacts():
    # Підготовка моків
    mock_db = AsyncMock(spec=AsyncSession)
    mock_contact = Contact(
        id=1,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        birthday=date(1990, 1, 1),
        created_at=datetime.utcnow()
    )
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_contact]
    mock_db.execute.return_value = mock_result

    # Виклик функції
    contact_service = ContactService(mock_db)
    contacts = await contact_service.search_contacts(first_name="John", last_name=None, email=None)

    # Перевірка результатів
    assert len(contacts) == 1
    assert isinstance(contacts[0], ContactResponse)
    assert contacts[0].first_name == "John"
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_upcoming_birthdays():
    # Підготовка моків
    mock_db = AsyncMock(spec=AsyncSession)
    mock_contact = Contact(
        id=1,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        birthday=date.today() + timedelta(days=3),  # День народження через 3 дні
        created_at=datetime.now(),
    )
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_contact]
    mock_db.execute.return_value = mock_result

    # Виклик функції
    contact_service = ContactService(mock_db)
    contacts = await contact_service.get_upcoming_birthdays(days=7)

    # Перевірка результатів
    assert len(contacts) == 1
    assert isinstance(contacts[0], ContactResponse)
    assert contacts[0].first_name == "John"
    mock_db.execute.assert_called_once()    


@pytest.mark.asyncio
async def test_get_contacts():
    # Підготовка моків
    mock_db = AsyncMock(spec=AsyncSession)
    mock_contact = Contact(
        id=1,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        birthday=date(1990, 1, 1),
        created_at=datetime.now(), 
    )
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_contact]
    mock_db.execute.return_value = mock_result

    # Виклик функції
    contact_service = ContactService(mock_db)
    contacts = await contact_service.get_contacts(user=None, skip=0, limit=100)

    # Перевірка результатів
    assert len(contacts) == 1
    assert isinstance(contacts[0], ContactResponse)
    assert contacts[0].first_name == "John"
    mock_db.execute.assert_called_once()    


@pytest.mark.asyncio
async def test_get_contact_by_id():
    # Підготовка моків
    mock_db = AsyncMock(spec=AsyncSession)
    mock_contact = Contact(
        id=1,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        birthday=date(1990, 1, 1),
        created_at=datetime.now(), 
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_contact
    mock_db.execute.return_value = mock_result

    # Виклик функції
    contact_service = ContactService(mock_db)
    contact = await contact_service.get_contact_by_id(contact_id=1)

    # Перевірка результатів
    assert isinstance(contact, ContactResponse)
    assert contact.first_name == "John"
    mock_db.execute.assert_called_once()


