from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.database.db import get_db

router = APIRouter(tags=["utils"])

@router.get("/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        # Виконуємо асинхронний запит до бази даних
        result = await db.execute(text("SELECT 1"))
        result = result.scalar_one_or_none()

        # Перевіряємо результат запиту
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "APP is healthy"}
    
    except Exception as e:
        # Виведення помилки у консоль
        print(f"Error: {e}")
        
        # Обробка помилок та повернення відповіді з кодом 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )

