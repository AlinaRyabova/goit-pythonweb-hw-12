from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi import  Request
from starlette.responses import JSONResponse

limiter = Limiter(key_func=get_remote_address)

  
