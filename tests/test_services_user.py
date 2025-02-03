import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.users import UserService
from src.schemas.users import UserCreate
from libgravatar import Gravatar

@pytest.mark.asyncio
async def test_create_user_success():
    # Підготовка моків
    mock_db = AsyncMock(spec=AsyncSession)
    mock_repository = AsyncMock()
    
    # Створення UserService з замоканим репозиторієм
    user_service = UserService(db=mock_db)
    user_service.repository = mock_repository
    
    user_create = UserCreate(username="testuser", email="test@example.com", password="password123")
    
    # Мокаємо метод для створення користувача в репозиторії
    mock_repository.create_user = AsyncMock(return_value={"id": 1, "username": "testuser", "email": "test@example.com"})
    
    # Мокаємо Gravatar
    with patch.object(Gravatar, 'get_image', return_value="http://avatar.url"):
        response = await user_service.create_user(user_create)

    # Перевірка, що метод репозиторію був викликаний правильно
    mock_repository.create_user.assert_called_once_with(user_create, "http://avatar.url")
    assert response == {"id": 1, "username": "testuser", "email": "test@example.com"}

@pytest.mark.asyncio
async def test_create_user_gravatar_error():
    # Підготовка моків
    mock_db = AsyncMock(spec=AsyncSession)
    mock_repository = AsyncMock()

    user_service = UserService(db=mock_db)
    user_service.repository = mock_repository
    
    user_create = UserCreate(username="testuser", email="test@example.com", password="password123")
    
    # Мокаємо метод для створення користувача в репозиторії
    mock_repository.create_user = AsyncMock(return_value={"id": 1, "username": "testuser", "email": "test@example.com"})
    
    # Мокаємо помилку при отриманні аватару
    with patch.object(Gravatar, 'get_image', side_effect=Exception("Gravatar error")):
        response = await user_service.create_user(user_create)

    # Перевірка, що метод репозиторію був викликаний з `None` аватаром
    mock_repository.create_user.assert_called_once_with(user_create, None)
    assert response == {"id": 1, "username": "testuser", "email": "test@example.com"}

@pytest.mark.asyncio
async def test_get_user_by_id():
    # Підготовка моків
    mock_db = AsyncMock(spec=AsyncSession)
    mock_repository = AsyncMock()

    user_service = UserService(db=mock_db)
    user_service.repository = mock_repository
    
    # Мокаємо повернення користувача
    mock_repository.get_user_by_id = AsyncMock(return_value={"id": 1, "username": "testuser", "email": "test@example.com"})
    
    response = await user_service.get_user_by_id(1)

    # Перевірка результату
    mock_repository.get_user_by_id.assert_called_once_with(1)
    assert response == {"id": 1, "username": "testuser", "email": "test@example.com"}

@pytest.mark.asyncio
async def test_get_user_by_username():
    # Підготовка моків
    mock_db = AsyncMock(spec=AsyncSession)
    mock_repository = AsyncMock()

    user_service = UserService(db=mock_db)
    user_service.repository = mock_repository
    
    # Мокаємо повернення користувача
    mock_repository.get_user_by_username = AsyncMock(return_value={"id": 1, "username": "testuser", "email": "test@example.com"})
    
    response = await user_service.get_user_by_username("testuser")

    # Перевірка результату
    mock_repository.get_user_by_username.assert_called_once_with("testuser")
    assert response == {"id": 1, "username": "testuser", "email": "test@example.com"}



@pytest.mark.asyncio
async def test_update_avatar_user_not_found():
    # Підготовка моків
    mock_db = AsyncMock(spec=AsyncSession)
    mock_repository = AsyncMock()

    user_service = UserService(db=mock_db)
    user_service.repository = mock_repository
    
    # Мокаємо повернення None для користувача
    mock_repository.get_user_by_id = AsyncMock(return_value=None)
    
    response = await user_service.update_avatar(1, "http://newavatar.url")

    # Перевірка, що не було оновлено аватар
    mock_repository.update_user.assert_not_called()
    assert response is None
