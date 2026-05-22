from fastapi import Request, HTTPException
from database import get_db

async def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        return None
    return token