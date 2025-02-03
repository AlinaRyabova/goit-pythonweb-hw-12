import pytest
from unittest.mock import AsyncMock, patch
from fastapi_mail import FastMail, MessageSchema
import httpx
from pydantic import EmailStr
from src.services.email import send_email, conf

@pytest.mark.asyncio
async def test_send_email_success():
    # Підготовка моків
    mock_fastmail = AsyncMock(spec=FastMail)
    mock_fastmail.send_message = AsyncMock()

    # Імітація успішного відправлення листа
    with patch("src.services.email.FastMail", return_value=mock_fastmail):
        await send_email(
            email="test@example.com",  # Замінили на простий рядок
            username="testuser",
            host="http://localhost",
        )

    # Перевірка, що send_message був викликаний
    mock_fastmail.send_message.assert_called_once()

@pytest.mark.asyncio
async def test_send_email_connection_error():
    # Підготовка моків
    mock_fastmail = AsyncMock(spec=FastMail)
    mock_fastmail.send_message = AsyncMock(side_effect=httpx.RequestError("Connection error"))

    # Імітація помилки підключення
    with patch("src.services.email.FastMail", return_value=mock_fastmail):
        # Використовуємо pytest.raises для перевірки, чи з'являється помилка
        with pytest.raises(httpx.RequestError):
            await send_email(
                email="test@example.com",
                username="testuser",
                host="http://localhost",
            )
    # Перевірка, що send_message був викликаний
    mock_fastmail.send_message.assert_called_once()

@pytest.mark.asyncio
async def test_send_email_with_correct_parameters():
    # Підготовка моків
    mock_fastmail = AsyncMock(spec=FastMail)
    mock_fastmail.send_message = AsyncMock()

    # Імітація виклику з правильними параметрами
    with patch("src.services.email.FastMail", return_value=mock_fastmail):
        await send_email(
            email="test@example.com",  # Замінили на простий рядок
            username="testuser",
            host="http://localhost",
        )

    # Перевірка, що send_message був викликаний з правильними параметрами
    mock_fastmail.send_message.assert_called_once()
    message: MessageSchema = mock_fastmail.send_message.call_args[0][0]
    assert message.recipients == ["test@example.com"]
    assert message.subject == "Confirm your email"
    assert message.template_body["username"] == "testuser"
    assert message.template_body["host"] == "http://localhost"
    assert "token" in message.template_body
