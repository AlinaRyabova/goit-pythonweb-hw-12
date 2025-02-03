import redis.asyncio as redis
from fastapi import Depends
from src.conf.config import settings

# Підключення до Redis
async def get_redis_client():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)
    return redis
  
