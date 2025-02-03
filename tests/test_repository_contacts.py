import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.models import Contact, User
from src.repository.contacts import ContactRepository

@pytest.mark.asyncio
async def test_get_contacts():
    # Підготовка моків
    mock_db = AsyncMock(spec=AsyncSession)
    mock_user = User(id=1)
    mock_contact = Contact(id=1, first_name="John", last_name="Doe", user=mock_user)

    # Створюємо мок для результату виконання запиту
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_contact]

    # Налаштовуємо mock_db.execute для повернення мокового результату
    mock_db.execute.return_value = mock_result

    # Виклик функції
    contact_repo = ContactRepository(mock_db)
    contacts = await contact_repo.get_contacts(user=mock_user, skip=0, limit=10)

    # Перевірка результатів
    assert len(contacts) == 1
    assert contacts[0].first_name == "John"
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_contact_by_id():
    # Підготовка моків
    mock_db = AsyncMock(spec=AsyncSession)
    mock_contact = Contact(id=1, first_name="John", last_name="Doe")
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_contact
    mock_db.execute.return_value = mock_result

    # Виклик функції
    contact_repo = ContactRepository(mock_db)
    contact = await contact_repo.get_contact_by_id(contact_id=1)

    # Перевірка результатів
    assert contact is not None
    assert contact.first_name == "John"
    mock_db.execute.assert_called_once()    

  