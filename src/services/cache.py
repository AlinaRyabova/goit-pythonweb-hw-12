import aioredis
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.services.redis import get_redis_client
from src.services.auth import get_current_user as get_current_user_from_db
from src.database.db import get_db
from src.schemas.users import User
import json

async def get_current_user(redis=Depends(get_redis_client), db: Session = Depends(get_db)) -> User:
    """
    Отримання поточного користувача.
    
    Спочатку перевіряється кеш в Redis. Якщо користувач знайдений, повертається він.
    Якщо в Redis немає користувача, здійснюється запит до бази даних, 
    та результати кешуються для подальшого використання.

    Args:
        redis (aioredis.Redis): Redis клієнт.
        db (Session): Сесія бази даних.

    Returns:
        User: Поточний користувач.
    """
    user_cache_key = "current_user"  # Можна використовувати ID користувача як частину ключа
    cached_user = await redis.get(user_cache_key)
    
    if cached_user:
        # Якщо дані знайдені в кеші, повертаємо користувача
        return User.parse_obj(json.loads(cached_user))

    # Якщо користувача в кеші немає, беремо його з бази даних
    user = await get_current_user_from_db(db)  # Отримуємо користувача з бази даних

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Зберігаємо дані користувача в кеш Redis на 1 годину
    await redis.set(user_cache_key, json.dumps(user.dict()), expire=3600)  # expire = 3600 секунд

    return user
