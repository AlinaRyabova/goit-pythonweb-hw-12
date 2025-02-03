import pytest
from src.services.auth import Hash
from datetime import datetime, timedelta, UTC
from src.services.auth import create_access_token
from src.conf.config import settings
from datetime import datetime, UTC
from src.services.auth import create_email_token
from src.conf.config import settings

def test_verify_password():
    hash = Hash()
    plain_password = "password123"
    hashed_password = hash.get_password_hash(plain_password)

    # Перевірка правильного пароля
    assert hash.verify_password(plain_password, hashed_password) is True

    # Перевірка неправильного пароля
    assert hash.verify_password("wrong_password", hashed_password) is False

def test_get_password_hash():
    hash = Hash()
    password = "password123"
    hashed_password = hash.get_password_hash(password)

    # Перевірка, що хеш не є порожнім
    assert hashed_password is not None
    assert isinstance(hashed_password, str)    



@pytest.mark.asyncio
async def test_create_access_token():
    data = {"sub": "testuser"}
    expires_delta = 3600  # 1 година

    # Виклик функції
    token = await create_access_token(data, expires_delta)

    # Перевірка результатів
    assert token is not None
    assert isinstance(token, str)

    # Перевірка, що токен містить дані
    from jose import jwt
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    assert payload["sub"] == "testuser"
    assert "exp" in payload    





def test_create_email_token():
    data = {"sub": "test@example.com"}

    # Виклик функції
    token = create_email_token(data)

    # Перевірка результатів
    assert token is not None
    assert isinstance(token, str)

    # Перевірка, що токен містить дані
    from jose import jwt
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    assert payload["sub"] == "test@example.com"
    assert "exp" in payload


